import json
import ollama
import platform
import psutil
import re
from .browser_controller import BrowserController

def get_system_specs():
    cpu_info = {
        'cores': psutil.cpu_count(logical=False),
        'logical_cores': psutil.cpu_count(logical=True),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().total / (1024 ** 3),  # Convert to GB
        'platform': platform.platform()
    }
    return cpu_info

def select_model(cpu_info):
    if cpu_info['logical_cores'] <= 4 or cpu_info['memory'] < 7:
        return 'tinyllama'
    else:
        return 'phi3'

class WebAgent:
    def __init__(self, ollama_host='http://127.0.0.1:11435', model=None):
        self.client = ollama.Client(host=ollama_host)
        if model is None:
            cpu_info = get_system_specs()
            print(f"System Specs: {cpu_info} | Selected Model: {select_model(cpu_info)}")
            self.model = select_model(cpu_info)
        else:
            self.model = model
        self.memory_file = 'data/memory.json'
        self.memory = self._load_memory()
        self.browser = BrowserController(headless=True)  # Headless for background execution

    def _load_memory(self):
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'tasks': [], 'last_task': ''}

    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def parse_and_plan(self, instruction):
        clean_instruction = re.sub(r'[^\w\s]', '', instruction).lower()

        # Fixed regex: Capture full multi-word terms before price
        search_pattern = re.compile(r'(find|search|look)\s+(?:for\s+)?(?:(amazon|flipkart)\s+)?([a-zA-Z0-9\s]+?)(?=\s+(under|below)\s+\d+\s*(inr|₹)?|$)', re.I)
        match = search_pattern.search(clean_instruction)

        if match:
            site = match.group(2) or 'amazon'
            terms = match.group(3).strip()  # Now captures "laptops" fully
            price_match = re.search(r'(under|below)\s+(\d+)\s*(inr|₹)?', clean_instruction, re.I)
            price = price_match.group(2) if price_match else None
            step = f"search_{site}_{terms.replace(' ', '_')}{f'_price_{price}' if price else ''}"
            print(f"Parsed instruction: '{instruction}' -> Step: '{step}'")  # Debug: Confirms full terms
            return {
                "steps": [step],
                "reasoning": "Direct pattern match for search query"
            }

        # LLM fallback
        prompt = f"""
        Parse this instruction into actionable steps:
        '{instruction}'

        Rules:
        1. For search queries, use: search_[website]_[terms]
        2. For navigation, use: navigate_[url]
        3. Default website is Amazon if not specified
        4. Include price filters if mentioned (e.g., _price_50000)

        Output JSON format: {{"steps": ["step1"], "reasoning": "explanation"}}
        """
        try:
            response = self.client.generate(model=self.model, prompt=prompt, options={"temperature": 0.2})
            plan = json.loads(response['response'])
            return plan
        except Exception as e:
            print(f"LLM parsing failed: {e}")
            return {
                "steps": [f"search_amazon_{instruction.replace(' ', '_')}"],
                "reasoning": "Fallback search command due to parsing error"
            }

    def execute_plan(self, plan, max_retries=3):
        results = []
        for step in plan['steps']:
            for attempt in range(max_retries):
                try:
                    result = self.browser.execute_action(step)
                    if isinstance(result, list) and not result:
                        result = ["No results found."]
                    results.append(result)
                    break
                except Exception as e:
                    error_msg = f"Retry {attempt+1}: {str(e)}"
                    print(error_msg)
                    if attempt == max_retries - 1:
                        results.append(f"Failed: {error_msg}")
        output = {'results': results, 'reasoning': plan.get('reasoning', 'No reasoning provided')}
        with open('data/results.json', 'w') as f:
            json.dump(output, f, indent=2)
        if results and all(isinstance(r, list) and all(isinstance(i, dict) for i in r) for r in results):
            import csv
            with open('data/results.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'price'])
                writer.writeheader()
                for result in results:
                    writer.writerows(result)
        return output

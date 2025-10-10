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
        'memory': psutil.virtual_memory().total,
        'platform': platform.platform()
    }
    return cpu_info

def select_model(cpu_info):
    if cpu_info['logical_cores'] <= 4 or cpu_info['memory'] < 8 * (1024 ** 3):
        return 'tinyllama'
    else:
        return 'llama2'

class WebAgent:
    def __init__(self, ollama_host='http://127.0.0.1:11435', model=None):
        self.client = ollama.Client(host=ollama_host)
        if model is None:
            cpu_info = get_system_specs()
            self.model = select_model(cpu_info)
        else:
            self.model = model
        self.memory_file = 'data/memory.json'
        self.memory = self._load_memory()
        self.browser = BrowserController(headless=False)

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
        # Pre-process instruction for better parsing
        clean_instruction = re.sub(r'[^\w\s]', '', instruction).lower()

        # Direct search pattern matching
        search_pattern = re.compile(r'(find|search|look)\s+(?:for\s+)?(?:(amazon|flipkart)\s+)?(.+?)(?:\s+(under|below)\s+(\d+)\s*(INR|₹))?', re.I)
        match = search_pattern.search(clean_instruction)

        if match:
            site = match.group(2) or 'amazon'
            terms = match.group(3)
            price = match.group(5) or None
            return {
                "steps": [f"search_{site}_{terms}{f'_price_{price}' if price else ''}"],
                "reasoning": "Direct pattern match for search query"
            }

        # LLM-based parsing as fallback
        prompt = f"""
        Parse this instruction into actionable steps:
        '{instruction}'

        Rules:
        1. For search queries, use: search_[website]_[terms]
        2. For navigation, use: navigate_[url]
        3. Default website is Amazon if not specified
        4. Include price filters if mentioned

        Output JSON format: {{"steps": ["step1"], "reasoning": "explanation"}}
        """

        try:
            response = self.client.generate(model=self.model, prompt=prompt)
            plan = json.loads(response['response'])
            return plan
        except:
            return {
                "steps": [f"search_amazon_{instruction}"],
                "reasoning": "Fallback search command"
            }

    def execute_plan(self, plan, max_retries=3):
        results = []
        for step in plan['steps']:
            for attempt in range(max_retries):
                try:
                    result = self.browser.execute_action(step)
                    results.append(result)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        results.append(f"Failed: {str(e)}")
                    print(f"Retry {attempt+1}: {str(e)}")

        output = {'results': results, 'reasoning': plan.get('reasoning', '')}
        with open('data/results.json', 'w') as f:
            json.dump(output, f, indent=2)
        return output

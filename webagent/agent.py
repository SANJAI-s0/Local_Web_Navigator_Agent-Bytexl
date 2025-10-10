import json
import ollama
import platform
import psutil
from .browser_controller import BrowserController

def get_system_specs():
    # Get CPU info
    cpu_info = {
        'cores': psutil.cpu_count(logical=False),
        'logical_cores': psutil.cpu_count(logical=True),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().total,
        'platform': platform.platform()
    }
    return cpu_info

def select_model(cpu_info):
    # Example logic to select model based on system specs
    if cpu_info['logical_cores'] <= 4 or cpu_info['memory'] < 8 * (1024 ** 3):  # Less than 4 cores or 8GB RAM
        return 'tinyllama'  # Lightweight model
    else:
        return 'llama2'  # More advanced model

class WebAgent:
    def __init__(self, ollama_host='http://127.0.0.1:11435', model=None):
        self.client = ollama.Client(host=ollama_host)
        if model is None:
            # Automatically select model based on system specs
            cpu_info = get_system_specs()
            self.model = select_model(cpu_info)
        else:
            self.model = model
        self.memory_file = 'data/memory.json'
        self.memory = self._load_memory()
        self.browser = BrowserController(headless=True)  # VM-isolated mode

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
        # Multi-step reasoning prompt
        prompt = f"""
        Parse this instruction into steps: {instruction}
        Use previous memory: {self.memory.get('last_task', '')}
        Output JSON: {{"steps": ["step1", "step2"], "reasoning": "brief explanation"}}
        """
        response = self.client.generate(model=self.model, prompt=prompt)
        try:
            plan = json.loads(response['response'])
        except json.JSONDecodeError:
            plan = {"steps": [instruction], "reasoning": "Direct execution due to parsing error"}
        self.memory['tasks'].append({'instruction': instruction, 'plan': plan})
        self.memory['last_task'] = instruction
        self._save_memory()
        return plan

    def execute_plan(self, plan, max_retries=3):
        results = []
        for step in plan['steps']:
            for attempt in range(max_retries):
                try:
                    # Execute step via browser (e.g., search, click)
                    result = self.browser.execute_action(step)
                    results.append(result)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        results.append(f"Failed after retries: {str(e)}")
                    print(f"Retry {attempt+1} for step: {step} (Error: {e})")
        # Structured output
        output = {'results': results, 'reasoning': plan['reasoning']}
        with open('data/results.json', 'w') as f:
            json.dump(output, f, indent=2)
        # Also export to CSV for simple tasks
        if all(isinstance(r, str) for r in results):
            import csv
            with open('data/results.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Results'])
                writer.writerows([[r] for r in results])
        return output

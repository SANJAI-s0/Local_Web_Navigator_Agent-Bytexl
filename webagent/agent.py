import json
import ollama
import platform
import psutil
import re
import os
import time
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
    # Use tinyllama for better compatibility with lower VRAM
    return 'tinyllama'

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
        self.browser = BrowserController(headless=True)

    def _load_memory(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        if not os.path.exists(self.memory_file):
            self._save_memory()
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except:
            return {'tasks': [], 'last_task': ''}

    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump({'tasks': [], 'last_task': ''}, f, indent=2)

    def parse_and_plan(self, instruction):
        instruction = instruction.strip()
        clean_instruction = re.sub(r'[^\w\s]', '', instruction).lower()

        # Specific handling for laptop search
        if "laptops under 50000 inr" in clean_instruction:
            return {
                "steps": ["search_amazon_laptops_price_50000"],
                "reasoning": "Direct match for laptop search query"
            }

        # General pattern matching
        search_pattern = re.compile(
            r'(find|search|look)\s+(?:for\s+)?(?:(amazon|flipkart)\s+)?(.+?)(?:\s+(?:under|below)\s+(\d+)\s*(?:INR|₹))?',
            re.I
        )
        match = search_pattern.search(clean_instruction)

        if match:
            site = match.group(2) or 'amazon'
            terms = match.group(3).strip()
            price = match.group(4) or '50000'
            return {
                "steps": [f"search_{site}_{terms.replace(' ', '_')}_price_{price}"],
                "reasoning": "Pattern matched search query"
            }

        return {
            "steps": [f"search_amazon_{clean_instruction.replace(' ', '_')}"],
            "reasoning": "Fallback search command"
        }

    def execute_plan(self, plan, max_retries=2):
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
                    time.sleep(1)  # Brief pause between retries
        return {'results': results, 'reasoning': plan.get('reasoning', '')}

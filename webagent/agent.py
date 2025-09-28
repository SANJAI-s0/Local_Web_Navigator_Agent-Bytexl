import ollama
import json
import os
from datetime import datetime
import time

class WebNavigatorAgent:
    def __init__(self):
        self.memory_file = 'memory.json'
        self.load_memory()

    def load_memory(self):
        """Load task history from memory.json."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.memory = json.load(f)
            except:
                self.memory = []
        else:
            self.memory = []

    def save_task(self, instruction, plan):
        """Save task to memory.json."""
        task = {
            'instruction': instruction,
            'plan': plan,
            'timestamp': datetime.now().isoformat()
        }
        self.memory.append(task)
        # Keep only the last 3 tasks
        self.memory = self.memory[-3:]
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def parse_instruction(self, user_input):
        """Parse user input into a plan using Ollama."""
        context_str = "\n".join([f"User: {task['instruction']}\nAgent: {task['plan']}" for task in self.memory])
        prompt = f"""
        Context from previous tasks:
        {context_str}

        User instruction: {user_input}

        Break this into a list of browser actions and specify what to extract.
        Example: For "search laptops under 50k and list top 5":
        ```json
        {{
            "steps": [
                "Navigate to https://www.google.com",
                "Type 'laptops under 50k' in search box",
                "Submit search",
                "Extract top 5 results (titles and links)"
            ],
            "extraction": "titles and links from search results"
        }}
        ```

        Output as JSON.
        """
        try:
            # Wait for server to initialize
            time.sleep(5)
            response = ollama.chat(
                model='tinyllama',
                messages=[{'role': 'user', 'content': prompt}],
                options={'server': 'http://127.0.0.1:11435'}
            )
            plan = json.loads(response['message']['content'])
        except Exception as e:
            print(f"Parsing error: {e}")
            plan = {"steps": [], "extraction": ""}
        return plan

    def execute_plan(self, plan, browser):
        """Execute the plan steps using the browser controller."""
        results = []
        for step in plan.get("steps", []):
            for attempt in range(3):  # Retry up to 3 times
                try:
                    if step.startswith("Navigate to"):
                        url = step.split("Navigate to ")[1].strip()
                        browser.navigate(url)
                    elif step.startswith("Type"):
                        parts = step.split(" in ")
                        text = parts[0].split("Type ")[1].strip("'")
                        selector = parts[1].strip()
                        browser.type_text(self.map_selector(selector), text)
                    elif step.startswith("Submit"):
                        browser.submit_form()
                    elif step.startswith("Extract"):
                        extracted = browser.extract_text(plan["extraction"])
                        results.extend(extracted)
                    break  # Success, exit retry loop
                except Exception as e:
                    print(f"Error in step '{step}' (attempt {attempt + 1}): {e}")
                    if attempt == 2:
                        results.append({"error": f"Failed step: {step}"})
        return results

    def map_selector(self, description):
        """Map natural language selector to CSS selector."""
        selector_map = {
            "search box": 'input[name="q"]',  # Google search
            "submit button": 'input[type="submit"]'
        }
        return selector_map.get(description, description)

from playwright.sync_api import sync_playwright
import time

class BrowserController:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None  # VM-like isolation

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(viewport={'width': 1920, 'height': 1080})  # Isolated "VM" context

    def execute_action(self, action):
        if not self.context:
            self.start()
        page = self.context.new_page()
        try:
            if 'search' in action.lower():
                # Example: Search on Amazon
                search_term = action.split('for ')[-1] if 'for ' in action else action
                page.goto('https://www.amazon.in')
                page.wait_for_load_state('networkidle')
                page.fill('input[name="field-keywords"]', search_term)
                page.click('input[type="submit"]')
                page.wait_for_load_state('networkidle')
                results = page.query_selector_all('.s-result-item h2')
                texts = [el.inner_text() for el in results[:5] if el]
                return texts
            elif 'click' in action.lower():
                # Placeholder for click actions
                return f"Clicked on element related to: {action}"
            elif 'extract' in action.lower():
                # Placeholder for text extraction
                return page.inner_text('body')[:500]  # Truncated example
            elif 'fill form' in action.lower():
                # Placeholder for form filling
                return f"Filled form with data from: {action}"
            else:
                page.goto(action) if action.startswith('http') else page.goto(f'https://{action}')
                return f"Navigated to: {page.url}"
        finally:
            page.close()
            time.sleep(1)  # Avoid rate limiting

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

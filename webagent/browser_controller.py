from playwright.sync_api import sync_playwright
import time
import re

class BrowserController:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True
        )

    def execute_action(self, action):
        if not self.context:
            self.start()
        page = self.context.new_page()

        try:
            # Handle search commands
            if action.startswith('search_'):
                parts = action.split('_', 2)
                site = parts[1].lower()
                query = '_'.join(parts[2:])

                # Extract price filter
                price = None
                if 'price_' in query:
                    query, price = query.split('price_', 1)
                    price = re.sub(r'[^\d]', '', price)

                query = query.replace('_', ' ')

                if site == 'amazon':
                    page.goto('https://www.amazon.in')
                    page.wait_for_load_state('networkidle')

                    # Handle login popup if exists
                    try:
                        page.click('button:has-text("Deliver to")', timeout=2000)
                    except:
                        pass

                    page.fill('input[name="field-keywords"]', query)
                    page.click('input[type="submit"]')
                    page.wait_for_load_state('networkidle')

                    # Apply price filter if specified
                    if price:
                        try:
                            page.click('span:has-text("Price: Low to High")')
                            page.wait_for_timeout(2000)
                        except:
                            pass

                    # Extract results
                    results = []
                    items = page.query_selector_all('.s-result-item')
                    for item in items[:5]:
                        title = item.query_selector('h2 a span')
                        price_elem = item.query_selector('.a-price .a-offscreen')
                        if title and price_elem:
                            results.append({
                                'title': title.inner_text().strip(),
                                'price': price_elem.inner_text().strip()
                            })
                    return results

                elif site == 'flipkart':
                    page.goto('https://www.flipkart.com')
                    page.wait_for_load_state('networkidle')

                    # Close login popup
                    try:
                        page.click('button._2KpZ6l._2doB4z', timeout=2000)
                    except:
                        pass

                    page.fill('input[name="q"]', query)
                    page.click('button[type="submit"]')
                    page.wait_for_load_state('networkidle')

                    # Extract results
                    results = []
                    items = page.query_selector_all('._1AtVbE')
                    for item in items[:5]:
                        title = item.query_selector('._4rR01T')
                        price_elem = item.query_selector('._30jeq3._1_WHN1')
                        if title and price_elem:
                            results.append({
                                'title': title.inner_text().strip(),
                                'price': price_elem.inner_text().strip()
                            })
                    return results

            # Handle navigation commands
            elif action.startswith('navigate_'):
                url = action[9:]
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                page.goto(url)
                return f"Navigated to: {page.url}"

            else:
                return f"Unknown command: {action}"

        finally:
            page.close()
            time.sleep(1)

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

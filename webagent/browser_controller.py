from playwright.sync_api import sync_playwright
import time
import re

class BrowserController:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.default_timeout = 60000

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True,
            extra_http_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )

    def execute_action(self, action):
        if not self.context:
            self.start()
        page = self.context.new_page()

        try:
            if action.startswith('search_'):
                parts = action.split('_', 2)
                site = parts[1].lower()
                query = '_'.join(parts[2:])

                price = None
                if 'price_' in query:
                    query, price = query.split('price_', 1)
                    price = re.sub(r'[^\d]', '', price)

                query = query.replace('_', ' ')
                print(f"Executing search on {site} for: '{query}' (price filter: {price})")

                if site == 'amazon':
                    page.goto('https://www.amazon.in', timeout=self.default_timeout)
                    page.wait_for_load_state('load', timeout=self.default_timeout)

                    try:
                        page.click('#nav-global-location-popover-link', timeout=2000) or page.click('button:has-text("Deliver to")', timeout=2000)
                        page.keyboard.press('Escape')
                    except:
                        pass

                    page.wait_for_selector('#twotabsearchtextbox', timeout=10000)
                    page.fill('#twotabsearchtextbox', query)
                    page.click('input[type="submit"]')
                    page.wait_for_load_state('load', timeout=self.default_timeout)

                    if price:
                        try:
                            page.click('a[href*="low-price&high-price=50000"]', timeout=5000)
                            page.wait_for_timeout(3000)
                        except:
                            print("Price filter failed.")

                    page.wait_for_selector('div.s-result-item', timeout=10000)
                    results = []
                    items = page.query_selector_all('div.s-result-item')
                    print(f"Found {len(items)} result items")
                    for item in items[:5]:
                        title = item.query_selector('h2 a span.a-size-medium.a-color-base.a-text-normal')
                        price_elem = item.query_selector('span.a-price span.a-offscreen')
                        if title and price_elem:
                            results.append({
                                'title': title.inner_text().strip(),
                                'price': price_elem.inner_text().strip()
                            })
                        elif title:
                            results.append({
                                'title': title.inner_text().strip(),
                                'price': 'Price N/A'
                            })
                    if not results:
                        fallback_items = page.query_selector_all('div[data-component-type="s-search-result"]')
                        for item in fallback_items[:5]:
                            title_text = item.query_selector('h2 span').inner_text().strip() if item.query_selector('h2 span') else 'N/A'
                            price_text = item.query_selector('.a-price-whole').inner_text().strip() if item.query_selector('.a-price-whole') else 'N/A'
                            results.append({
                                'title': title_text,
                                'price': price_text
                            })
                    return results or ["No results found or extraction failed."]

                elif site == 'flipkart':
                    page.goto('https://www.flipkart.com', timeout=self.default_timeout)
                    page.wait_for_load_state('load', timeout=self.default_timeout)

                    try:
                        page.click('button._2KpZ6l._2doB4z', timeout=2000)
                    except:
                        pass

                    page.wait_for_selector('input[name="q"]', timeout=10000)
                    page.fill('input[name="q"]', query)
                    page.click('button[type="submit"]')
                    page.wait_for_load_state('load', timeout=self.default_timeout)

                    page.wait_for_selector('._1AtVbE', timeout=10000)
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
                    return results or ["No results found or extraction failed."]

            elif action.startswith('navigate_'):
                # Fixed indentation: Indented block here
                url = action[9:]
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                page.goto(url, timeout=self.default_timeout)
                page.wait_for_load_state('load', timeout=self.default_timeout)
                return f"Navigated to: {page.url}"

            else:
                # Fixed indentation: Indented block here
                return f"Unknown command: {action}"

        except Exception as e:
            print(f"Browser action failed for '{action}': {str(e)}")
            return f"Failed: {str(e)}"
        finally:
            page.close()
            time.sleep(2)

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

from playwright.sync_api import sync_playwright
import time

class BrowserController:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.timeout = 60000  # Increased timeout to 60 seconds

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            timeout=self.timeout,
            args=['--disable-gpu', '--no-sandbox']  # Additional stability flags
        )
        self.context = self.browser.new_context(
            viewport={'width': 1280, 'height': 800},  # Smaller viewport
            ignore_https_errors=True,
            bypass_csp=True  # Bypass content security policies
        )

    def execute_action(self, action):
        if not self.context:
            self.start()

        page = self.context.new_page()
        try:
            if action.startswith('search_amazon_'):
                # Parse the action
                parts = action.split('_')
                terms = '_'.join(parts[2:-2]) if len(parts) > 2 else 'laptops'
                price = parts[-1] if len(parts) > 2 else '50000'

                # Clean terms
                terms = terms.replace('_', ' ')

                # Navigate to Amazon
                page.goto('https://www.amazon.in', timeout=self.timeout)
                page.wait_for_load_state('networkidle', timeout=self.timeout)

                # Handle popups
                try:
                    close_btn = page.get_by_role('button', name='Deliver to')
                    if close_btn:
                        close_btn.click(timeout=2000)
                except:
                    pass

                # Enter search terms
                search_box = page.get_by_role('combobox', name='Search Amazon.in')
                if search_box:
                    search_box.fill(terms)
                    page.get_by_role('button', name='Go').click()
                    page.wait_for_load_state('networkidle', timeout=self.timeout)

                    # Filter by price
                    try:
                        price_filter = page.get_by_text('Price: Low to High')
                        if price_filter:
                            price_filter.click(timeout=5000)
                            time.sleep(2)  # Wait for filter to apply
                    except:
                        pass

                    # Extract results
                    results = []
                    items = page.get_by_role('listitem').all()[:5]
                    for item in items:
                        try:
                            title = item.get_by_role('heading').inner_text()
                            price_elem = item.get_by_role('link', name='Price').inner_text()
                            results.append({'title': title.strip(), 'price': price_elem.strip()})
                        except:
                            continue

                    return results if results else "No results found"

            return f"Unknown command: {action}"

        except Exception as e:
            return f"Error: {str(e)}"

        finally:
            page.close()
            time.sleep(1)

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

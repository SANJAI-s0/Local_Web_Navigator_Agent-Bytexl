from playwright.sync_api import sync_playwright

class BrowserController:
    def __init__(self, headless=True):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def navigate(self, url):
        """Navigate to a URL."""
        self.page.goto(url, timeout=30000)

    def type_text(self, selector, text):
        """Type text into an element."""
        self.page.fill(selector, text)

    def submit_form(self):
        """Submit a form (e.g., press Enter on search)."""
        self.page.press('input[name="q"]', 'Enter')

    def extract_text(self, extraction_desc):
        """Extract text based on description."""
        if "titles and links from search results" in extraction_desc:
            elements = self.page.query_selector_all('.tF2Cxc')  # Google results
            results = []
            for el in elements[:5]:
                try:
                    title = el.query_selector('h3').inner_text()
                    link = el.query_selector('a').get_attribute('href')
                    results.append({"title": title, "link": link})
                except:
                    continue
            return results
        return []

    def close(self):
        """Close the browser."""
        self.browser.close()
        self.p.stop()
        
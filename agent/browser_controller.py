# agent/browser_controller.py
"""
Playwright-based browser controller (sync).
Designed to run locally on Windows.

Features:
- Start/stop browser safely
- Google/DuckDuckGo/Flipkart search
- Safe navigation, extraction, and actions
- Lightweight error handling and logging
"""

import time
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class BrowserController:
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self._play = None
        self._browser = None
        self._context = None
        self.page = None

    # -------------------- Lifecycle --------------------
    def start(self):
        """Start Playwright and browser session."""
        if self.page:  # already started
            return

        self._play = sync_playwright().start()
        self._browser = self._play.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context()
        self.page = self._context.new_page()
        self.page.set_default_timeout(self.timeout)

    def stop(self):
        """Stop browser session and clean resources."""
        for obj in [self._context, self._browser, self._play]:
            try:
                if obj:
                    obj.close() if hasattr(obj, "close") else obj.stop()
            except Exception:
                pass
        self._play = self._browser = self._context = self.page = None

    # -------------------- Core Actions --------------------
    def goto(self, url: str) -> bool:
        """Navigate to a URL safely. Returns success status."""
        try:
            self.page.goto(url)
            time.sleep(1)
            return True
        except PlaywrightTimeoutError:
            print(f"[Timeout] Failed to load {url}")
        except Exception as e:
            print(f"[Error] goto({url}): {e}")
        return False

    def search(self, engine: str, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a web search (DuckDuckGo preferred, Google may block).
        Returns: list of {title, url, snippet}.
        """
        url = f"https://duckduckgo.com/?q={query}" if engine.lower() == "duckduckgo" else f"https://www.google.com/search?q={query}"
        if not self.goto(url):
            return []

        results = []
        try:
            if engine.lower() == "duckduckgo":
                containers = self.page.query_selector_all("div.results--main div.result")
                count = 0
                for c in containers:
                    if count >= max_results:
                        break
                    link = c.query_selector("a.result__a")
                    snippet_el = c.query_selector("a.result__snippet") or c.query_selector("div.result__snippet")
                    results.append({
                        "title": link.inner_text() if link else "",
                        "url": link.get_attribute("href") if link else "",
                        "snippet": snippet_el.inner_text() if snippet_el else ""
                    })
                    count += 1

            elif engine.lower() == "google":
                containers = self.page.query_selector_all("div.g")
                for c in containers[:max_results]:
                    title = c.query_selector("h3")
                    link = c.query_selector("a")
                    snippet = c.query_selector("div.IsZvec")
                    results.append({
                        "title": title.inner_text() if title else None,
                        "url": link.get_attribute("href") if link else None,
                        "snippet": snippet.inner_text() if snippet else ""
                    })
        except Exception as e:
            print(f"[Error] search(): {e}")

        return results

    def extract_text(self, selector: str) -> List[str]:
        """Extract inner text of elements matching a selector."""
        try:
            self.page.wait_for_selector(selector, timeout=5000)
            elements = self.page.query_selector_all(selector)
            print(f"[Debug] Found {len(elements)} elements for selector '{selector}'")
            texts = [e.inner_text() for e in elements]
            print(f"[Debug] Extracted texts sample: {texts[:5]}")
            return texts
        except Exception as e:
            print(f"[Error] extract_text({selector}): {e}")
            return []

    def click(self, selector: str) -> bool:
        """Click an element. Returns success."""
        try:
            self.page.click(selector)
            return True
        except Exception as e:
            print(f"[Error] click({selector}): {e}")
            return False

    def fill(self, selector: str, value: str) -> bool:
        """Fill an input field. Returns success."""
        try:
            self.page.fill(selector, value)
            return True
        except Exception as e:
            print(f"[Error] fill({selector}): {e}")
            return False

    def screenshot(self, path: str = "screenshot.png") -> Optional[str]:
        """Take a screenshot and return file path."""
        try:
            self.page.screenshot(path=path)
            return path
        except Exception as e:
            print(f"[Error] screenshot({path}): {e}")
            return None

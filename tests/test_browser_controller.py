# test_browser_controller.py
"""
Quick test for BrowserController.
Runs: start -> search -> goto -> extract -> screenshot -> stop
"""

from agent.browser_controller import BrowserController


def main():
    bc = BrowserController(headless=True)  # set False if you want to see browser window
    bc.start()

    print("\n--- DuckDuckGo Search Test ---")
    results = bc.search("duckduckgo", "OpenAI ChatGPT", max_results=3)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']} -> {r['url']}")

    if results:
        print("\n--- Navigation Test ---")
        bc.goto(results[0]["url"])
        text = bc.extract_text("h1, h2, h3")
        print("Extracted headings:", text[:5])

    print("\n--- Screenshot Test ---")
    screenshot_path = bc.screenshot("test_screenshot.png")
    if screenshot_path:
        print(f"Screenshot saved at: {screenshot_path}")

    bc.stop()
    print("\nAll tests completed.")


if __name__ == "__main__":
    main()

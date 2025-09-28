# tests/test_browser_controller.py
import pytest
from webagent.browser_controller import BrowserController

@pytest.fixture
def browser():
    bc = BrowserController(headless=True)
    yield bc
    bc.close()

def test_navigate(browser):
    """Test navigation to a URL."""
    browser.navigate("https://www.example.com")
    assert browser.page.url == "https://www.example.com/"

def test_type_text(browser):
    """Test typing text into an element.

    Use a small data: URL with a known input element instead of relying on external sites.
    """
    # a tiny HTML page served via data: URL containing an input[name="q"]
    html_data_url = "data:text/html,<html><body><input name='q' id='q'></body></html>"
    browser.navigate(html_data_url)
    browser.type_text('input[name="q"]', "test query")
    value = browser.page.evaluate('document.querySelector("input[name=\'q\']").value')
    assert value == "test query"

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
    """Test typing text into an element."""
    browser.navigate("https://www.google.com")
    browser.type_text('input[name="q"]', "test query")
    value = browser.page.evaluate('document.querySelector("input[name=\'q\']").value')
    assert value == "test query"

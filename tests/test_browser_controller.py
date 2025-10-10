import pytest
from webagent.browser_controller import BrowserController

@pytest.fixture
def controller():
    bc = BrowserController(headless=True)
    yield bc
    bc.stop()

def test_execute_action_search(controller):
    result = controller.execute_action("search for laptops under 50k")
    assert isinstance(result, list)
    assert len(result) > 0

def test_execute_action_navigate(controller):
    result = controller.execute_action("https://example.com")
    assert "Navigated to" in result

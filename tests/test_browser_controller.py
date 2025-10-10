import pytest
from webagent.browser_controller import BrowserController
import time

@pytest.fixture
def controller():
    return BrowserController(headless=True)

def test_browser_controller_initialization(controller):
    assert isinstance(controller, BrowserController)
    assert controller.headless is True
    assert controller.timeout == 10000

def test_search_command(controller):
    # Test Amazon search command
    result = controller.execute_action("search_amazon_laptops")
    assert isinstance(result, (list, str))

    # Test with price filter
    result = controller.execute_action("search_amazon_laptops_price_50000")
    assert isinstance(result, (list, str))

def test_navigation_command(controller):
    # Test URL navigation
    result = controller.execute_action("navigate_https://example.com")
    assert isinstance(result, str)
    assert "Navigated to:" in result

def test_unknown_command(controller):
    # Test unknown command
    result = controller.execute_action("unknown_command")
    assert isinstance(result, str)
    assert "Unknown command" in result

def test_timeout_handling(controller):
    # Test with very short timeout
    original_timeout = controller.timeout
    controller.timeout = 1  # 1ms timeout (should fail)

    try:
        result = controller.execute_action("search_amazon_test")
        # Should return error due to timeout
        assert isinstance(result, str)
    finally:
        controller.timeout = original_timeout

def test_context_management(controller):
    # Test context start/stop
    assert controller.context is None
    controller.start()
    assert controller.context is not None
    controller.stop()
    assert controller.context is None

def test_multiple_actions(controller):
    # Test executing multiple actions
    actions = [
        "search_amazon_books",
        "navigate_https://example.com"
    ]

    for action in actions:
        result = controller.execute_action(action)
        assert isinstance(result, (list, str))

import pytest
from webagent.agent import WebAgent

@pytest.fixture
def agent():
    return WebAgent(model='tinyllama')  # Assume Ollama is running

def test_parse_and_plan(agent):
    plan = agent.parse_and_plan("search for laptops under 50k")
    assert 'steps' in plan
    assert isinstance(plan['steps'], list)

def test_execute_plan(agent):
    plan = {"steps": ["search for laptops under 50k"], "reasoning": "Test"}
    results = agent.execute_plan(plan)
    assert 'results' in results
    assert len(results['results']) > 0

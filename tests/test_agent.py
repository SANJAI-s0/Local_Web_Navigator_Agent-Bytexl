import pytest
from webagent.agent import WebAgent
import json
import os

@pytest.fixture
def agent():
    # Use test memory file
    os.makedirs('data', exist_ok=True)
    with open('data/memory.json', 'w') as f:
        json.dump({'tasks': [], 'last_task': ''}, f)
    return WebAgent()

def test_agent_initialization(agent):
    assert isinstance(agent, WebAgent)
    assert agent.model in ['tinyllama', 'llama2']

def test_parse_and_plan(agent):
    # Test basic search query
    plan = agent.parse_and_plan("Find laptops under 50000 INR")
    assert isinstance(plan, dict)
    assert 'steps' in plan
    assert 'reasoning' in plan
    assert len(plan['steps']) > 0

    # Test with specific site
    plan = agent.parse_and_plan("Search Flipkart for smartphones")
    assert isinstance(plan, dict)
    assert 'steps' in plan

    # Test with price filter
    plan = agent.parse_and_plan("Look for headphones below 2000 INR")
    assert isinstance(plan, dict)
    assert 'steps' in plan

def test_memory_operations(agent):
    # Test memory load and save
    initial_memory = agent.memory.copy()
    test_instruction = "Test instruction"

    # Execute a test instruction
    plan = agent.parse_and_plan(test_instruction)

    # Verify memory was updated
    assert len(agent.memory['tasks']) > 0
    assert agent.memory['last_task'] == test_instruction

    # Verify memory file was created
    assert os.path.exists('data/memory.json')

def test_execute_plan(agent):
    # Test with simple search query
    plan = agent.parse_and_plan("Find books on Python")
    results = agent.execute_plan(plan)

    assert isinstance(results, dict)
    assert 'results' in results
    assert 'reasoning' in results
    assert len(results['results']) > 0

def test_system_specs_detection():
    from webagent.agent import get_system_specs, select_model
    specs = get_system_specs()

    # Basic validation of system specs
    assert 'cores' in specs
    assert 'logical_cores' in specs
    assert 'memory' in specs

    # Test model selection
    model = select_model(specs)
    assert model in ['tinyllama', 'llama2']

def test_error_handling(agent):
    # Test with malformed instruction
    plan = agent.parse_and_plan("")  # Empty instruction
    assert isinstance(plan, dict)
    assert 'steps' in plan

    # Test with special characters
    plan = agent.parse_and_plan("!@#$%^&*()")
    assert isinstance(plan, dict)
    assert 'steps' in plan

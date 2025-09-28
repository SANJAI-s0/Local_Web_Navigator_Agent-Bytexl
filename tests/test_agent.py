import pytest
import json
import os
from webagent.agent import WebNavigatorAgent

@pytest.fixture
def agent(tmp_path):
    memory_file = tmp_path / "memory.json"
    agent = WebNavigatorAgent()
    agent.memory_file = str(memory_file)
    agent.load_memory()
    yield agent

def test_parse_instruction(agent, mocker):
    """Test instruction parsing (mock Ollama)."""
    mocker.patch('webagent.agent.ollama.chat', return_value={
        'message': {
            'content': json.dumps({
                "steps": ["Navigate to https://www.google.com", "Type 'test' in search box"],
                "extraction": "titles and links"
            })
        }
    })
    plan = agent.parse_instruction("search for test")
    assert plan["steps"] == ["Navigate to https://www.google.com", "Type 'test' in search box"]
    assert plan["extraction"] == "titles and links"

def test_map_selector(agent):
    """Test selector mapping."""
    assert agent.map_selector("search box") == 'input[name="q"]'
    assert agent.map_selector("unknown") == "unknown"

def test_save_task(agent):
    """Test saving a task to memory.json."""
    agent.save_task("test instruction", json.dumps({"steps": [], "extraction": ""}))
    assert os.path.exists(agent.memory_file)
    with open(agent.memory_file, 'r') as f:
        memory = json.load(f)
    assert len(memory) == 1
    assert memory[0]["instruction"] == "test instruction"

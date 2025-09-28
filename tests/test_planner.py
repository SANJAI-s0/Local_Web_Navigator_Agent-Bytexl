# tests/test_planner.py
import pytest
from agent.planner import Planner

def test_heuristic_plan_non_empty():
    p = Planner()
    plan = p.plan("Search for cheap laptops under 50000 INR")
    assert isinstance(plan, dict)
    assert "task_id" in plan
    assert "actions" in plan and isinstance(plan["actions"], list)
    assert plan["actions"][0]["type"] in ("search", "open_url")

def test_invalid_instruction_raises():
    p = Planner()
    with pytest.raises(ValueError):
        p.plan("")  # empty instruction should raise

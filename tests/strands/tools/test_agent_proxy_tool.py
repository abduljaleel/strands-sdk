import pytest
from unittest.mock import MagicMock

from strands.agent.agent import Agent
from strands.agent.agent_result import AgentResult
from strands.tools.agent_proxy_tool import AgentProxyTool


@pytest.fixture
def mock_agent():
    agent = MagicMock(spec=Agent)
    agent_result = AgentResult(
        "end_turn",
        {"role": "assistant", "content": [{"text": "pong"}]},
        {},
        {},
    )
    agent.return_value = agent_result
    agent.__call__.return_value = agent_result
    return agent


@pytest.fixture
def agent_tool(mock_agent):
    return AgentProxyTool(name="helper", agent=mock_agent)


def test_tool_name(agent_tool):
    assert agent_tool.tool_name == "helper"


def test_tool_type(agent_tool):
    assert agent_tool.tool_type == "python"


def test_tool_spec(agent_tool):
    spec = agent_tool.tool_spec
    assert spec["name"] == "helper"
    assert "message" in spec["inputSchema"]["json"]["properties"]


def test_invoke(agent_tool, mock_agent):
    tool_use = {"toolUseId": "t1", "name": "helper", "input": {"message": "ping"}}
    result = agent_tool.invoke(tool_use)
    mock_agent.assert_called_once_with("ping")
    assert result["toolUseId"] == "t1"
    assert result["status"] == "success"
    assert result["content"] == [{"text": "pong"}]

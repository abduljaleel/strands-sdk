"""Agent proxy tool for inter-agent communication."""

from typing import Any, Optional

from ..agent import AgentResult, Agent
from ..types.tools import AgentTool, ToolResult, ToolSpec, ToolUse


class AgentProxyTool(AgentTool):
    """Wrap another :class:`~strands.agent.Agent` as a tool."""

    def __init__(self, name: str, agent: Agent, description: Optional[str] = None) -> None:
        super().__init__()
        self._name = name
        self.agent = agent
        self._description = description or f"Send a message to agent '{name}'"

    @property
    def tool_name(self) -> str:
        return self._name

    @property
    def tool_spec(self) -> ToolSpec:
        return {
            "name": self._name,
            "description": self._description,
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                    "required": ["message"],
                }
            },
        }

    @property
    def tool_type(self) -> str:
        return "python"

    def invoke(self, tool: ToolUse, *args: Any, **kwargs: dict[str, Any]) -> ToolResult:
        message = tool.get("input", {}).get("message", "")
        result: AgentResult = self.agent(message)
        return {
            "toolUseId": tool.get("toolUseId", "unknown"),
            "status": "success",
            "content": result.message.get("content", []),
        }

from dataclasses import dataclass
from typing import Any
from langgraph.types import Command
from backend.schemas import TurnSummary
from backend.messages import last_ai_text, last_tool_text

@dataclass
class AgentTurnResult:
    text: str
    structured: TurnSummary | None
    messages: list[Any]
    pending_interrupt: dict[str, Any] | None

def parse_invoke_result(result: Any) -> AgentTurnResult:
    interrupts = tuple(getattr(result, "interrupts", ()) or ())
    value = getattr(result, "value", result)
    if not isinstance(value, dict):
        value = {}
        
    messages = value.get("messages") or []
    
    if interrupts:
        payload = interrupts[0].value
        return AgentTurnResult(
            text="",
            structured=None,
            messages=messages,
            pending_interrupt=payload if isinstance(payload, dict) else {"raw": payload}
        )

    return AgentTurnResult(
        text=last_ai_text(messages) or last_tool_text(messages),
        structured=value.get("structured_response"),
        messages=messages,
        pending_interrupt=None
    )

def start_turn(agent, user_text: str, config: dict) -> AgentTurnResult:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_text}]},
        config=config,
        version="v2"
    )
    return parse_invoke_result(result)

def resume_turn(agent, decisions: list[dict], config: dict) -> AgentTurnResult:
    result = agent.invoke(
        Command(resume={"decisions": decisions}),
        config=config,
        version="v2"
    )
    return parse_invoke_result(result)
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langgraph.checkpoint.memory import InMemorySaver
from backend.config import MAX_MODEL_CALLS_PER_RUN, hitl_enabled
from backend.middlewares import AuditMiddleware, build_hitl_middleware
from backend.models import build_chat_model
from backend.memory import make_checkpointer
from backend.prompts import build_system_prompt
from backend.schemas import TurnSummary
from backend.tools import ALL_TOOLS

def build_middleware(enable_hitl: bool) -> list:
    layers = [
        ModelCallLimitMiddleware(
            run_limit=MAX_MODEL_CALLS_PER_RUN,
            exit_behavior="end"
        ),
        AuditMiddleware(),
    ]
    if enable_hitl:
        layers.append(build_hitl_middleware())
    return layers

def build_agent(
    checkpointer: InMemorySaver | None = None,
    enable_hitl: bool | None = None,
):
    model, provider = build_chat_model()
    use_hitl = hitl_enabled() if enable_hitl is None else enable_hitl

    return create_agent(
        model=model,
        tools=ALL_TOOLS,
        system_prompt=build_system_prompt(),
        middleware=build_middleware(enable_hitl=use_hitl),
        #response_format=ProviderStrategy(TurnSummary),
        checkpointer=checkpointer or make_checkpointer(),
        name="Ticketmaster-Event-Agent",
    )
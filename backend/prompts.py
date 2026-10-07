from jinja2 import Environment, FileSystemLoader, select_autoescape
from backend.config import PROMPTS_DIR, AGENT_NAME
from backend.tools import tool_catalog

_env = Environment(
    loader=FileSystemLoader(PROMPTS_DIR),
    autoescape=select_autoescape(enabled_extensions=()),
    trim_blocks=True,
    lstrip_blocks=True,
)

def build_system_prompt(agent_name: str = AGENT_NAME) -> str:
    return _env.get_template("system.jinja").render(
        agent_name=agent_name,
        tools=tool_catalog(),
    )
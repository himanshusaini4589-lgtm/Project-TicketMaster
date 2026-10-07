import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


@dataclass(frozen=True)
class Provider:
    name: str
    env_var: str
    is_free: bool
    model: str


PROVIDERS = [
    Provider(
        name="Groq",
        env_var="GROQ_API_KEY",
        is_free=True,
        model="openai/gpt-oss-120b",
    )
]


def select_provider() -> Provider:
    for provider in PROVIDERS:
        if os.getenv(provider.env_var):
            return provider

    raise RuntimeError("GROQ_API_KEY missing in .env file.")


def build_chat_model() -> tuple[ChatGroq, Provider]:
    provider = select_provider()

    model = ChatGroq(
        model=provider.model,
        api_key=os.getenv(provider.env_var),
        temperature=0.0,
    )

    return model, provider
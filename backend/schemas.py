from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

class TurnSummary(BaseModel):
    summary: str = Field(
        description="A concise summary of what event searches, details, or booking approvals occurred in this turn."
    )
    files_touched: list[str] = Field(
        description="List of tool names called in this turn (e.g. ['search_events', 'proceed_to_booking']).",
        default_factory=list,
    )
    status: Literal["ok", "needs_input", "failed"] = Field(
        description="ok if turn completed; needs_input if waiting for HITL approval or user info; failed if an error occurred."
    )
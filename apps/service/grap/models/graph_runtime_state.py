from typing import Any

from pydantic import BaseModel, Field

from apps.service.grap.models.variable_pool import VariablePool


class GraphRuntimeState(BaseModel):
    variable_pool: VariablePool = Field(..., description="variable pool")
    """variable pool"""

    start_at: float = Field(..., description="start time")
    """start time"""
    total_tokens: int = 0

    """llm usage info"""
    outputs: dict[str, Any] = {}
    """outputs"""

    node_run_steps: int = 0
    """node run steps"""

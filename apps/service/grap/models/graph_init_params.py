from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, Field

from apps.service.grap.engine.workflow_type import WorkflowType


class GraphInitParams(BaseModel):
    # init params
    tenant_id: str = Field(..., description="tenant / workspace id")
    app_id: str = Field(..., description="app id")
    workflow_type: WorkflowType = Field(..., description="workflow type")
    workflow_id: str = Field(..., description="workflow id")
    graph_config: Mapping[str, Any] = Field(..., description="graph config")
    user_id: str = Field(..., description="user id")
    call_depth: int = Field(..., description="call depth")

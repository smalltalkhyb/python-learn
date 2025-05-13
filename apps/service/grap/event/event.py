from datetime import datetime

from pydantic import BaseModel, Field

from apps.service.grap.engine.workflow_type import WorkflowNodeExecutionStatus
from apps.service.grap.models.node_entities import NodeRunResult


class RunCompletedEvent(BaseModel):
    run_result: NodeRunResult = Field(..., description="run result")


class RunStreamChunkEvent(BaseModel):
    chunk_content: str = Field(..., description="chunk content")
    from_variable_selector: list[str] = Field(..., description="from variable selector")


class RunRetrieverResourceEvent(BaseModel):
    retriever_resources: list[dict] = Field(..., description="retriever resources")
    context: str = Field(..., description="context")


class ModelInvokeCompletedEvent(BaseModel):
    """
    Model invoke completed
    """

    text: str
    finish_reason: str | None = None


class RunRetryEvent(BaseModel):
    """Node Run Retry event"""

    error: str = Field(..., description="error")
    retry_index: int = Field(..., description="Retry attempt number")
    start_at: datetime = Field(..., description="Retry start time")


class SingleStepRetryEvent(NodeRunResult):
    """Single step retry event"""

    status: WorkflowNodeExecutionStatus = WorkflowNodeExecutionStatus.RETRY

    elapsed_time: float = Field(..., description="elapsed time")

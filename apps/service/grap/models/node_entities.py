from collections.abc import Mapping
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel

from apps.service.grap.engine.workflow_type import WorkflowNodeExecutionStatus


class NodeRunMetadataKey(Enum):
    """
    Node Run Metadata Key.
    """

    TOTAL_TOKENS = "total_tokens"
    TOTAL_PRICE = "total_price"
    CURRENCY = "currency"
    TOOL_INFO = "tool_info"
    AGENT_LOG = "agent_log"
    ITERATION_ID = "iteration_id"
    ITERATION_INDEX = "iteration_index"
    LOOP_ID = "loop_id"
    LOOP_INDEX = "loop_index"
    PARALLEL_ID = "parallel_id"
    PARALLEL_START_NODE_ID = "parallel_start_node_id"
    PARENT_PARALLEL_ID = "parent_parallel_id"
    PARENT_PARALLEL_START_NODE_ID = "parent_parallel_start_node_id"
    PARALLEL_MODE_RUN_ID = "parallel_mode_run_id"
    ITERATION_DURATION_MAP = "iteration_duration_map"  # single iteration duration if iteration node runs
    LOOP_DURATION_MAP = "loop_duration_map"  # single loop duration if loop node runs
    ERROR_STRATEGY = "error_strategy"  # node in continue on error mode return the field
    LOOP_VARIABLE_MAP = "loop_variable_map"  # single loop variable output


class NodeRunResult(BaseModel):
    """
    Node Run Result.
    """

    status: WorkflowNodeExecutionStatus = WorkflowNodeExecutionStatus.RUNNING

    inputs: Optional[Mapping[str, Any]] = None  # node inputs
    process_data: Optional[Mapping[str, Any]] = None  # process data
    outputs: Optional[Mapping[str, Any]] = None  # node outputs
    metadata: Optional[Mapping[NodeRunMetadataKey, Any]] = None  # node metadata

    edge_source_handle: Optional[str] = None  # source handle id of node with multiple branches

    error: Optional[str] = None  # error message if status is failed
    error_type: Optional[str] = None  # error type if status is failed

    # single step node run retry
    retry_index: int = 0


class AgentNodeStrategyInit(BaseModel):
    name: str
    icon: str | None = None

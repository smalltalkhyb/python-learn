"""
@Author: huyanbing
@Date: 2025/5/12
@Description: 
"""
from enum import Enum


class WorkflowType(Enum):
    """
    Workflow Type Enum
    """

    WORKFLOW = "workflow"
    CHAT = "chat"



class WorkflowNodeExecutionStatus(Enum):
    """
    Workflow Node Execution Status Enum
    """

    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    EXCEPTION = "exception"
    RETRY = "retry"
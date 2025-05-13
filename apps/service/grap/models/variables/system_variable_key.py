"""
@Author: huyanbing
@Date: 2025/5/12
@Description: 
"""
from enum import Enum


class SystemVariableKey(Enum):
    """
    System Variables.
    """

    QUERY = "query"
    FILES = "files"
    CONVERSATION_ID = "conversation_id"
    USER_ID = "user_id"
    DIALOGUE_COUNT = "dialogue_count"
    APP_ID = "app_id"
    WORKFLOW_ID = "workflow_id"
    WORKFLOW_RUN_ID = "workflow_run_id"

"""
@Author: huyanbing
@Date: 2025/5/12
@Description: 
"""
from enum import Enum


class NodeType(Enum):
    START = "start"
    END = "end"
    ANSWER = "answer"
    LLM = "llm"
    KNOWLEDGE_RETRIEVAL = "knowledge-retrieval"
    IF_ELSE = "if-else"
    CODE = "code"
    TEMPLATE_TRANSFORM = "template-transform"
    QUESTION_CLASSIFIER = "question-classifier"
    HTTP_REQUEST = "http-request"
    TOOL = "tool"
    VARIABLE_AGGREGATOR = "variable-aggregator"
    LEGACY_VARIABLE_AGGREGATOR = "variable-assigner"  # TODO: Merge this into VARIABLE_AGGREGATOR in the database.
    LOOP = "loop"
    LOOP_START = "loop-start"
    LOOP_END = "loop-end"
    ITERATION = "iteration"
    ITERATION_START = "iteration-start"  # Fake start node for iteration.
    PARAMETER_EXTRACTOR = "parameter-extractor"
    VARIABLE_ASSIGNER = "assigner"
    DOCUMENT_EXTRACTOR = "document-extractor"
    LIST_OPERATOR = "list-operator"
    AGENT = "agent"



class ErrorStrategy(Enum):
    FAIL_BRANCH = "fail-branch"
    DEFAULT_VALUE = "default-value"


class FailBranchSourceHandle(Enum):
    FAILED = "fail-branch"
    SUCCESS = "success-branch"


CONTINUE_ON_ERROR_NODE_TYPE = [NodeType.LLM, NodeType.CODE, NodeType.TOOL, NodeType.HTTP_REQUEST]
RETRY_ON_ERROR_NODE_TYPE = CONTINUE_ON_ERROR_NODE_TYPE
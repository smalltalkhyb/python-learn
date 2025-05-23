"""
@Author: huyanbing
@Date: 2025/5/12
@Description: 
"""
from typing import Literal, Sequence

from pydantic import BaseModel, Field

from apps.service.grap.default_type_value import BaseNodeData

SupportedComparisonOperator = Literal[
    # for string or array
    "contains",
    "not contains",
    "start with",
    "end with",
    "is",
    "is not",
    "empty",
    "not empty",
    "in",
    "not in",
    "all of",
    # for number
    "=",
    "≠",
    ">",
    "<",
    "≥",
    "≤",
    "null",
    "not null",
    # for file
    "exists",
    "not exists",
]


class SubCondition(BaseModel):
    key: str
    comparison_operator: SupportedComparisonOperator
    value: str | Sequence[str] | None = None


class SubVariableCondition(BaseModel):
    logical_operator: Literal["and", "or"]
    conditions: list[SubCondition] = Field(default=list)



class VariableSelector(BaseModel):
    """
    Variable Selector.
    """

    variable: str
    value_selector: Sequence[str]






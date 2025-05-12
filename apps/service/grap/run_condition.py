"""
@Author: huyanbing
@Date: 2025/5/12
@Description: 
"""
from typing import Literal, Optional, Sequence
import hashlib
from pydantic import BaseModel

from apps.service.grap.graph_entities import SupportedComparisonOperator, SubVariableCondition


class Condition(BaseModel):
    variable_selector: list[str]
    comparison_operator: SupportedComparisonOperator
    value: str | Sequence[str] | None = None
    sub_variable_condition: SubVariableCondition | None = None

class RunCondition(BaseModel):
    type: Literal["branch_identify", "condition"]
    """condition type"""

    branch_identify: Optional[str] = None
    """branch identify like: sourceHandle, required when type is branch_identify"""

    conditions: Optional[list[Condition]] = None
    """conditions to run the node, required when type is condition"""

    @property
    def hash(self) -> str:
        return hashlib.sha256(self.model_dump_json().encode()).hexdigest()

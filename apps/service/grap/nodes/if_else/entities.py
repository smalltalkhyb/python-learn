from typing import Literal, Optional

from pydantic import BaseModel, Field

from apps.service.grap.default_type_value import BaseNodeData
from apps.service.grap.models.variables.variable_entity import Condition


class IfElseNodeData(BaseNodeData):
    """
    If Else Node Data.
    """

    class Case(BaseModel):
        """
        Case entity representing a single logical condition group
        """

        case_id: str
        logical_operator: Literal["and", "or"]
        conditions: list[Condition]

    logical_operator: Optional[Literal["and", "or"]] = "and"
    conditions: Optional[list[Condition]] = Field(default=None, deprecated=True)

    cases: Optional[list[Case]] = None

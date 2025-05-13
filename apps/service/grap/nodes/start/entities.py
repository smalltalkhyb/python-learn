from collections.abc import Sequence

from pydantic import Field

from apps.service.grap.default_type_value import BaseNodeData
from apps.service.grap.models.variables.variable_entity import VariableEntity


class StartNodeData(BaseNodeData):
    """
    Start Node Data
    """

    variables: Sequence[VariableEntity] = Field(default_factory=list)

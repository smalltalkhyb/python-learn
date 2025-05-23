from typing import Literal, Optional

from pydantic import BaseModel

from apps.service.grap.default_type_value import BaseNodeData


class AdvancedSettings(BaseModel):
    """
    Advanced setting.
    """

    group_enabled: bool

    class Group(BaseModel):
        """
        Group.
        """

        output_type: Literal["string", "number", "object", "array[string]", "array[number]", "array[object]"]
        variables: list[list[str]]
        group_name: str

    groups: list[Group]


class VariableAssignerNodeData(BaseNodeData):
    """
    Variable Assigner Node Data.
    """

    type: str = "variable-assigner"
    output_type: str
    variables: list[list[str]]
    advanced_settings: Optional[AdvancedSettings] = None

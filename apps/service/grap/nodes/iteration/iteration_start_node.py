from apps.service.grap.engine.workflow_type import WorkflowNodeExecutionStatus
from apps.service.grap.models.node_entities import NodeRunResult
from apps.service.grap.models.node_model import BaseNode
from apps.service.grap.node_type import NodeType
from apps.service.grap.nodes.iteration.entities import IterationStartNodeData


class IterationStartNode(BaseNode[IterationStartNodeData]):
    """
    Iteration Start Node.
    """

    _node_data_cls = IterationStartNodeData
    _node_type = NodeType.ITERATION_START

    def _run(self) -> NodeRunResult:
        """
        Run the node.
        """
        return NodeRunResult(status=WorkflowNodeExecutionStatus.SUCCEEDED)

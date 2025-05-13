from apps.service.grap.engine.workflow_type import WorkflowNodeExecutionStatus
from apps.service.grap.models.node_entities import NodeRunResult
from apps.service.grap.models.node_model import BaseNode
from apps.service.grap.models.variables.variables_constants import SYSTEM_VARIABLE_NODE_ID
from apps.service.grap.node_type import NodeType
from apps.service.grap.nodes.start.entities import StartNodeData


class StartNode(BaseNode[StartNodeData]):
    _node_data_cls = StartNodeData
    _node_type = NodeType.START

    def _run(self) -> NodeRunResult:
        node_inputs = dict(self.graph_runtime_state.variable_pool.user_inputs)
        system_inputs = self.graph_runtime_state.variable_pool.system_variables

        # TODO: System variables should be directly accessible, no need for special handling
        # Set system variables as node outputs.
        for var in system_inputs:
            node_inputs[SYSTEM_VARIABLE_NODE_ID + "." + var] = system_inputs[var]

        return NodeRunResult(status=WorkflowNodeExecutionStatus.SUCCEEDED, inputs=node_inputs, outputs=node_inputs)

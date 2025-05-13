from apps.service.grap.engine.workflow_type import WorkflowNodeExecutionStatus
from apps.service.grap.models.node_entities import NodeRunResult
from apps.service.grap.models.node_model import BaseNode
from apps.service.grap.node_type import NodeType
from apps.service.grap.nodes.variable_aggregator.entities import VariableAssignerNodeData


class VariableAggregatorNode(BaseNode[VariableAssignerNodeData]):
    _node_data_cls = VariableAssignerNodeData
    _node_type = NodeType.VARIABLE_AGGREGATOR

    def _run(self) -> NodeRunResult:
        # Get variables
        outputs = {}
        inputs = {}

        if not self.node_data.advanced_settings or not self.node_data.advanced_settings.group_enabled:
            for selector in self.node_data.variables:
                variable = self.graph_runtime_state.variable_pool.get(selector)
                if variable is not None:
                    outputs = {"output": variable.to_object()}

                    inputs = {".".join(selector[1:]): variable.to_object()}
                    break
        else:
            for group in self.node_data.advanced_settings.groups:
                for selector in group.variables:
                    variable = self.graph_runtime_state.variable_pool.get(selector)

                    if variable is not None:
                        outputs[group.group_name] = {"output": variable.to_object()}
                        inputs[".".join(selector[1:])] = variable.to_object()
                        break

        return NodeRunResult(status=WorkflowNodeExecutionStatus.SUCCEEDED, outputs=outputs, inputs=inputs)

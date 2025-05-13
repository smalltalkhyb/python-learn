from typing import Literal

from typing_extensions import deprecated

from apps.infrastructure.utils.condition.entities import Condition
from apps.infrastructure.utils.condition.processor import ConditionProcessor
from apps.service.grap.engine.workflow_type import WorkflowNodeExecutionStatus
from apps.service.grap.models.node_entities import NodeRunResult
from apps.service.grap.models.node_model import BaseNode
from apps.service.grap.models.variable_pool import VariablePool
from apps.service.grap.node_type import NodeType
from apps.service.grap.nodes.if_else.entities import IfElseNodeData


class IfElseNode(BaseNode[IfElseNodeData]):
    _node_data_cls = IfElseNodeData
    _node_type = NodeType.IF_ELSE

    def _run(self) -> NodeRunResult:
        """
        Run node
        :return:
        """
        node_inputs: dict[str, list] = {"conditions": []}

        process_data: dict[str, list] = {"condition_results": []}

        input_conditions = []
        final_result = False
        selected_case_id = None
        condition_processor = ConditionProcessor()
        try:
            # Check if the new cases structure is used
            if self.node_data.cases:
                for case in self.node_data.cases:
                    input_conditions, group_result, final_result = condition_processor.process_conditions(
                        variable_pool=self.graph_runtime_state.variable_pool,
                        conditions=case.conditions,
                        operator=case.logical_operator,
                    )

                    process_data["condition_results"].append(
                        {
                            "group": case.model_dump(),
                            "results": group_result,
                            "final_result": final_result,
                        }
                    )

                    # Break if a case passes (logical short-circuit)
                    if final_result:
                        selected_case_id = case.case_id  # Capture the ID of the passing case
                        break

            else:
                # TODO: Update database then remove this
                # Fallback to old structure if cases are not defined
                input_conditions, group_result, final_result = _should_not_use_old_function(
                    condition_processor=condition_processor,
                    variable_pool=self.graph_runtime_state.variable_pool,
                    conditions=self.node_data.conditions or [],
                    operator=self.node_data.logical_operator or "and",
                )

                selected_case_id = "true" if final_result else "false"

                process_data["condition_results"].append(
                    {"group": "default", "results": group_result, "final_result": final_result}
                )

            node_inputs["conditions"] = input_conditions

        except Exception as e:
            return NodeRunResult(
                status=WorkflowNodeExecutionStatus.FAILED, inputs=node_inputs, process_data=process_data, error=str(e)
            )

        outputs = {"result": final_result, "selected_case_id": selected_case_id}

        data = NodeRunResult(
            status=WorkflowNodeExecutionStatus.SUCCEEDED,
            inputs=node_inputs,
            process_data=process_data,
            edge_source_handle=selected_case_id or "false",  # Use case ID or 'default'
            outputs=outputs,
        )

        return data


@deprecated("This function is deprecated. You should use the new cases structure.")
def _should_not_use_old_function(
    *,
    condition_processor: ConditionProcessor,
    variable_pool: VariablePool,
    conditions: list[Condition],
    operator: Literal["and", "or"],
):
    return condition_processor.process_conditions(
        variable_pool=variable_pool,
        conditions=conditions,
        operator=operator,
    )

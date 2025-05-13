"""
@Author: huyanbing
@Date: 2025/5/12
@Description: 
"""
from unittest.mock import patch

from apps.service.grap.engine.graph_engine import GraphEngine
from apps.service.grap.engine.workflow_type import WorkflowType, WorkflowNodeExecutionStatus
from apps.service.grap.event.event import RunStreamChunkEvent, RunCompletedEvent
from apps.service.grap.graph import Graph
from apps.service.grap.models.event import NodeRunSucceededEvent, NodeRunFailedEvent, GraphRunFailedEvent, \
    BaseNodeEvent, GraphRunStartedEvent, NodeRunStartedEvent
from apps.service.grap.models.node_entities import NodeRunResult, NodeRunMetadataKey
from apps.service.grap.models.runtime_route_state import RouteNodeState
from apps.service.grap.models.variable_pool import VariablePool
from apps.service.grap.models.variables.system_variable_key import SystemVariableKey

#
# @patch("extensions.ext_database.db.session.remove")
# @patch("extensions.ext_database.db.session.close")
def test_run_parallel_in_workflow():
    graph_config = {
        "edges": [
            {
                "id": "1",
                "source": "start",
                "target": "llm1",
            },
            {
                "id": "2",
                "source": "llm1",
                "target": "llm2",
            },
            {
                "id": "3",
                "source": "llm1",
                "target": "llm3",
            },
            {
                "id": "4",
                "source": "llm2",
                "target": "end1",
            },
            {
                "id": "5",
                "source": "llm3",
                "target": "end2",
            },
        ],
        "nodes": [
            {
                "data": {
                    "type": "start",
                    "title": "start",
                    "variables": [
                        {
                            "label": "query",
                            "max_length": 48,
                            "options": [],
                            "required": True,
                            "type": "text-input",
                            "variable": "query",
                        }
                    ],
                },
                "id": "start",
            },
            {
                "data": {
                    "type": "llm",
                    "title": "llm1",
                    "context": {"enabled": False, "variable_selector": []},
                    "model": {
                        "completion_params": {"temperature": 0.7},
                        "mode": "chat",
                        "name": "gpt-4o",
                        "provider": "openai",
                    },
                    "prompt_template": [
                        {"role": "system", "text": "say hi"},
                        {"role": "user", "text": "{{#start.query#}}"},
                    ],
                    "vision": {"configs": {"detail": "high", "variable_selector": []}, "enabled": False},
                },
                "id": "llm1",
            },
            {
                "data": {
                    "type": "llm",
                    "title": "llm2",
                    "context": {"enabled": False, "variable_selector": []},
                    "model": {
                        "completion_params": {"temperature": 0.7},
                        "mode": "chat",
                        "name": "gpt-4o",
                        "provider": "openai",
                    },
                    "prompt_template": [
                        {"role": "system", "text": "say bye"},
                        {"role": "user", "text": "{{#start.query#}}"},
                    ],
                    "vision": {"configs": {"detail": "high", "variable_selector": []}, "enabled": False},
                },
                "id": "llm2",
            },
            {
                "data": {
                    "type": "llm",
                    "title": "llm3",
                    "context": {"enabled": False, "variable_selector": []},
                    "model": {
                        "completion_params": {"temperature": 0.7},
                        "mode": "chat",
                        "name": "gpt-4o",
                        "provider": "openai",
                    },
                    "prompt_template": [
                        {"role": "system", "text": "say good morning"},
                        {"role": "user", "text": "{{#start.query#}}"},
                    ],
                    "vision": {"configs": {"detail": "high", "variable_selector": []}, "enabled": False},
                },
                "id": "llm3",
            },
            {
                "data": {
                    "type": "end",
                    "title": "end1",
                    "outputs": [
                        {"value_selector": ["llm2", "text"], "variable": "result2"},
                        {"value_selector": ["start", "query"], "variable": "query"},
                    ],
                },
                "id": "end1",
            },
            {
                "data": {
                    "type": "end",
                    "title": "end2",
                    "outputs": [
                        {"value_selector": ["llm1", "text"], "variable": "result1"},
                        {"value_selector": ["llm3", "text"], "variable": "result3"},
                    ],
                },
                "id": "end2",
            },
        ],
    }

    graph = Graph.init(graph_config=graph_config)

    variable_pool = VariablePool(
        system_variables={SystemVariableKey.FILES: [], SystemVariableKey.USER_ID: "aaa"}, user_inputs={"query": "hi"}
    )

    graph_engine = GraphEngine(
        tenant_id="111",
        app_id="222",
        workflow_type=WorkflowType.WORKFLOW,
        workflow_id="333",
        graph_config=graph_config,
        user_id="444",
        call_depth=0,
        graph=graph,
        variable_pool=variable_pool,
        max_execution_steps=500,
        max_execution_time=1200,
    )

    def llm_generator(self):
        contents = ["hi", "bye", "good morning"]

        yield RunStreamChunkEvent(
            chunk_content=contents[int(self.node_id[-1]) - 1], from_variable_selector=[self.node_id, "text"]
        )

        yield RunCompletedEvent(
            run_result=NodeRunResult(
                status=WorkflowNodeExecutionStatus.SUCCEEDED,
                inputs={},
                process_data={},
                outputs={},
                metadata={
                    NodeRunMetadataKey.TOTAL_TOKENS: 1,
                    NodeRunMetadataKey.TOTAL_PRICE: 1,
                    NodeRunMetadataKey.CURRENCY: "USD",
                },
            )
        )

    # print("")


    items = []
    generator = graph_engine.run()
    for item in generator:
        # print(type(item), item)
        items.append(item)
        if isinstance(item, NodeRunSucceededEvent):
            assert item.route_node_state.status == RouteNodeState.Status.SUCCESS

        assert not isinstance(item, NodeRunFailedEvent)
        assert not isinstance(item, GraphRunFailedEvent)

        if isinstance(item, BaseNodeEvent) and item.route_node_state.node_id in {"llm2", "llm3", "end1", "end2"}:
            assert item.parallel_id is not None

    assert len(items) == 18
    assert isinstance(items[0], GraphRunStartedEvent)
    assert isinstance(items[1], NodeRunStartedEvent)
    assert items[1].route_node_state.node_id == "start"
    assert isinstance(items[2], NodeRunSucceededEvent)
    assert items[2].route_node_state.node_id == "start"
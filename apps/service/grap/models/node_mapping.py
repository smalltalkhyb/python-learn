from collections.abc import Mapping

from apps.service.grap.models.node_model import BaseNode
from apps.service.grap.node_type import NodeType
from apps.service.grap.nodes.end import EndNode
from apps.service.grap.nodes.if_else import IfElseNode
from apps.service.grap.nodes.iteration import IterationNode
from apps.service.grap.nodes.start import StartNode
from apps.service.grap.nodes.variable_aggregator import VariableAggregatorNode

LATEST_VERSION = "latest"

NODE_TYPE_CLASSES_MAPPING: Mapping[NodeType, Mapping[str, type[BaseNode]]] = {
    NodeType.START: {
        LATEST_VERSION: StartNode,
        "1": StartNode,
    },
    NodeType.END: {
        LATEST_VERSION: EndNode,
        "1": EndNode,
    },
    NodeType.IF_ELSE: {
        LATEST_VERSION: IfElseNode,
        "1": IfElseNode,
    },
    NodeType.VARIABLE_AGGREGATOR: {
        LATEST_VERSION: VariableAggregatorNode,
        "1": VariableAggregatorNode,
    },
    NodeType.LEGACY_VARIABLE_AGGREGATOR: {
        LATEST_VERSION: VariableAggregatorNode,
        "1": VariableAggregatorNode,
    },  # original name of VARIABLE_AGGREGATOR
    NodeType.ITERATION: {
        LATEST_VERSION: IterationNode,
        "1": IterationNode,
    }
}

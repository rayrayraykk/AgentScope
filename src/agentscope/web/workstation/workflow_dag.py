# -*- coding: utf-8 -*-
# pylint: disable=R0912,R0915
"""
AgentScope workstation DAG running engine.

This module defines various workflow nodes that can be used to construct
a computational DAG. Each node represents a step in the DAG and
can perform certain actions when called.
"""
import copy
from typing import Any
from loguru import logger

import agentscope
from agentscope.web.workstation.workflow_node import (
    NODE_NAME_MAPPING,
    WorkflowNodeType,
)


try:
    import networkx as nx
except ImportError:
    nx = None


class ASDiGraph(nx.DiGraph):
    """
    A class that represents a directed graph, extending the functionality of
    networkx's DiGraph to suit specific workflow requirements in AgentScope.

    This graph supports operations such as adding nodes with associated
    computations and executing these computations in a topological order.

    Attributes:
        nodes_not_in_graph (set): A set of nodes that are not included in
        the computation graph.
    """

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the ASDiGraph instance.
        """
        super().__init__(*args, **kwargs)
        self.nodes_not_in_graph = set()

    def run(self, **kwargs: Any) -> None:
        """
        Execute the computations associated with each node in the graph.

        The method initializes AgentScope, performs a topological sort of
        the nodes, and then runs each node's computation sequentially using
        the outputs from its predecessors as inputs.
        """

        agentscope.init(
            logger_level="DEBUG",
            studio_url="http://127.0.0.1:5000",
            **kwargs,
        )
        sorted_nodes = list(nx.topological_sort(self))
        sorted_nodes = [
            node_id
            for node_id in sorted_nodes
            if node_id not in self.nodes_not_in_graph
        ]
        logger.info(f"sorted_nodes: {sorted_nodes}")
        logger.info(f"nodes_not_in_graph: {self.nodes_not_in_graph}")

        # Cache output
        values = {}

        root_node_ids = [
            node_id for node_id in sorted_nodes if self.in_degree(node_id) == 0
        ]
        start_node_ids = []
        model_node_ids = []
        for node_id in root_node_ids:
            if self.nodes[node_id]["opt"].node_type == WorkflowNodeType.START:
                start_node_ids.append(node_id)
            elif (
                self.nodes[node_id]["opt"].node_type == WorkflowNodeType.MODEL
            ):
                model_node_ids.append(node_id)

        if len(start_node_ids) <= 0:
            raise ValueError("No start node found!")

        from collections import deque

        node_queue = deque(start_node_ids)
        visited = set()
        values = {}

        while node_queue:
            node_id = node_queue.popleft()
            if node_id in visited:
                continue
            if all(
                predecessor in visited
                for predecessor in self.predecessors(node_id)
            ):
                inputs = [
                    values[predecessor]
                    for predecessor in self.predecessors(node_id)
                ]
                if not inputs:
                    values[node_id] = self.exec_node(node_id)
                elif len(inputs) == 1:
                    # Note: only support exec with the first predecessor now
                    values[node_id] = self.exec_node(node_id, inputs[0])
                elif len(inputs) > 1:
                    values[node_id] = self.exec_node(node_id, inputs)
                else:
                    raise ValueError("Too many predecessors!")

                visited.add(node_id)
                if (
                    self.nodes[node_id]["opt"].node_type
                    == WorkflowNodeType.IFELSE
                ):
                    node_info = self.nodes[node_id]
                    branch_true = values[node_id].get("branch", True)
                    next_node_ids = []
                    if branch_true:
                        next_node_ids = [
                            connection["node"]
                            for connection in node_info["outputs"][
                                "output_1"
                            ].get("connections", [])
                        ]
                    else:
                        next_node_ids = [
                            connection["node"]
                            for connection in node_info["outputs"][
                                "output_2"
                            ].get("connections", [])
                        ]
                    for child_id in next_node_ids:
                        if child_id not in visited:
                            node_queue.append(child_id)
                else:
                    for child_id in self.adj[node_id].keys():
                        if child_id not in visited:
                            node_queue.append(child_id)
            else:
                node_queue.append(node_id)

    # pylint: disable=R0912
    def add_as_node(
        self,
        node_id: str,
        node_info: dict,
        config: dict,
    ) -> Any:
        """
        Add a node to the graph based on provided node information and
        configuration.

        Args:
            node_id (str): The identifier for the node being added.
            node_info (dict): A dictionary containing information about the
                node.
            config (dict): Configuration information for the node dependencies.

        Returns:
            The computation object associated with the added node.
        """
        node_cls = NODE_NAME_MAPPING[node_info.get("name", "")]
        if node_cls.node_type not in [
            WorkflowNodeType.MODEL,
            WorkflowNodeType.AGENT,
            WorkflowNodeType.MESSAGE,
            WorkflowNodeType.PIPELINE,
            WorkflowNodeType.COPY,
            WorkflowNodeType.SERVICE,
            WorkflowNodeType.TOOL,
            WorkflowNodeType.START,
            WorkflowNodeType.IFELSE,
        ]:
            raise NotImplementedError(node_cls)

        if self.has_node(node_id):
            return self.nodes[node_id]["opt"]

        # Init dep nodes
        deps = [str(n) for n in node_info.get("data", {}).get("elements", [])]

        # Exclude for dag when in a Group
        if node_cls.node_type != WorkflowNodeType.COPY:
            self.nodes_not_in_graph = self.nodes_not_in_graph.union(set(deps))

        dep_opts = []
        for dep_node_id in deps:
            if not self.has_node(dep_node_id):
                dep_node_info = config[dep_node_id]
                self.add_as_node(
                    node_id=dep_node_id,
                    node_info=dep_node_info,
                    config=config,
                )
            dep_opts.append(self.nodes[dep_node_id]["opt"])

        node_opt = node_cls(
            node_id=node_id,
            opt_kwargs=node_info["data"].get("args", {}),
            source_kwargs=node_info["data"].get("source", {}),
            dep_opts=dep_opts,
        )

        self.add_node(
            node_id,
            opt=node_opt,
            **node_info,
        )

        return node_opt

    def exec_node(self, node_id: str, x_in: Any = None) -> Any:
        """
        Execute the computation associated with a given node in the graph.

        Args:
            node_id (str): The identifier of the node whose computation is
                to be executed.
            x_in: The input to the node's computation. Defaults to None.

        Returns:
            The output of the node's computation.
        """
        logger.debug(
            f"\nnode_id: {node_id}\nin_values:{x_in}",
        )
        opt = self.nodes[node_id]["opt"]
        out_values = opt(x_in)
        logger.debug(
            f"\nnode_id: {node_id}\nout_values:{out_values}",
        )
        return out_values


def sanitize_node_data(raw_info: dict) -> dict:
    """
    Clean and validate node data, evaluating callable expressions where
    necessary.

    Processes the raw node information, removes empty arguments, and evaluates
    any callable expressions provided as string literals.

    Args:
        raw_info (dict): The raw node information dictionary that may contain
            callable expressions as strings.

    Returns:
        dict: The sanitized node information with callable expressions
            evaluated.
    """

    copied_info = copy.deepcopy(raw_info)
    raw_info["data"]["source"] = copy.deepcopy(
        copied_info["data"].get(
            "args",
            {},
        ),
    )
    for key, value in copied_info["data"].get("args", {}).items():
        if value == "":
            raw_info["data"]["args"].pop(key)
            raw_info["data"]["source"].pop(key)
    return raw_info


def build_dag(config: dict) -> ASDiGraph:
    """
    Construct a Directed Acyclic Graph (DAG) from the provided configuration.

    Initializes the graph nodes based on the configuration, adds model nodes
    first, then non-model nodes, and finally adds edges between the nodes.

    Args:
        config (dict): The configuration to build the graph from, containing
            node info such as name, type, arguments, and connections.

    Returns:
        ASDiGraph: The constructed directed acyclic graph.

    Raises:
        ValueError: If the resulting graph is not acyclic.
    """
    dag = ASDiGraph()

    if (
        "drawflow" in config
        and "Home" in config["drawflow"]
        and "data" in config["drawflow"]["Home"]
    ):
        config = config["drawflow"]["Home"]["data"]

        config = {
            k: v
            for k, v in config.items()
            if not ("class" in v and v["class"] == "welcome")
        }

    for node_id, node_info in config.items():
        config[node_id] = sanitize_node_data(node_info)

    # Add and init model nodes first
    for node_id, node_info in config.items():
        if (
            NODE_NAME_MAPPING[node_info["name"]].node_type
            == WorkflowNodeType.MODEL
        ):
            dag.add_as_node(
                node_id,
                node_info,
                config,
            )

    # Add and init non-model nodes
    for node_id, node_info in config.items():
        if (
            NODE_NAME_MAPPING[node_info["name"]].node_type
            != WorkflowNodeType.MODEL
        ):
            dag.add_as_node(
                node_id,
                node_info,
                config,
            )

    # Add edges
    for node_id, node_info in config.items():
        inputs = node_info.get("inputs", {})
        for input_key, input_val in inputs.items():
            connections = input_val.get("connections", [])
            for conn in connections:
                target_node_id = conn.get("node")
                dag.add_edge(target_node_id, node_id, input_key=input_key)

    # Check if the graph is a DAG
    if not nx.is_directed_acyclic_graph(dag):
        raise ValueError("The provided configuration does not form a DAG.")

    return dag

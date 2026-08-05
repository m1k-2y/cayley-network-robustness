'''Simulate graph attacks and record robustness metrics at each step.'''
from typing import TypedDict
from collections.abc import Hashable
import networkx as nx
import random

class AttackStep(TypedDict):
    removed_fraction: float
    remaining_nodes: int
    component_count: int
    giant_component_size: int
    giant_component_ratio: float
    removed_item: Hashable | None

AttackHistory = list[AttackStep]

def measure_attack_step(
    graph: nx.Graph,
    initial_node_count: int,
    removed_fraction: float,
    removed_item: Hashable | None = None,
) -> AttackStep:
    '''Measure one attack step relative to the initial graph size.'''

    if initial_node_count <= 0:
        raise ValueError("initial_node_count must be positive.")

    component_count = 0
    giant_component_size = 0

    for component in nx.connected_components(graph):
        component_count += 1

        if len(component) >= giant_component_size:
            giant_component_size = len(component)
    
    step : AttackStep = {
        "removed_fraction": removed_fraction,
        "remaining_nodes": graph.number_of_nodes(),
        "component_count": component_count,
        "giant_component_size": giant_component_size,
        "giant_component_ratio": giant_component_size / initial_node_count,
        "removed_item": removed_item,
    }

    return step

def simulate_random_node_failure(
    graph: nx.Graph,
) -> AttackHistory:
    '''Randomly remove nodes from a graph copy and record each attack step.'''

    initial_node_count = graph.number_of_nodes()
    working_graph = graph.copy()
    history : AttackHistory = []

    while working_graph.number_of_nodes() > 0:
       removed_node = random.choice(list(working_graph.nodes))
       working_graph.remove_node(removed_node)

       removed_fraction = (initial_node_count - working_graph.number_of_nodes()) / initial_node_count
       removed_item = removed_node

       step = measure_attack_step(working_graph, initial_node_count, removed_fraction, removed_item)

       history.append(step)

    return history
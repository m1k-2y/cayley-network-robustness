'''Simulate graph attacks and record robustness metrics at each step.'''
from typing import TypedDict
from _collections_abc import Hashable
import networkx as nx
from src.metrics import compute_giant_component_ratio

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

    step : AttackStep = {}

    step['removed_fraction'] = removed_fraction
    step['remaining_nodes'] = graph.number_of_nodes()
    step['component_count'] = nx.number_connected_components(graph)

    giant_component_size = 0
    for component in nx.connected_components(graph):
        if len(component) > giant_component_size:
            giant_component_size = len(component)

    step['giant_component_size'] = giant_component_size

    step['giant_component_ratio'] = giant_component_size / initial_node_count
    step['removed_item'] = removed_item  

    return step  
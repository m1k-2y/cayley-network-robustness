'''Simulate graph attacks and record robustness metrics at each step.'''
from typing import TypedDict
from collections.abc import Hashable
from src.metrics import compute_component_sizes
from src.metrics import compute_shortest_path_metrics
import networkx as nx
import random
import time

class AttackStep(TypedDict):
    removed_fraction: float
    removed_count: int
    remaining_nodes: int
    remaining_edges: int
    component_count: int
    largest_component_size: int
    largest_component_ratio: float
    second_largest_component_size: int
    second_largest_component_ratio: float
    removed_item: Hashable | None
    diameter_lcc: int | None
    average_shortest_path_length_lcc: float | None
    global_efficiency: float | None
    runtime_seconds: float

AttackHistory = list[AttackStep]

def build_path_metric_checkpoints(
    initial_item_count: int,
) -> set[int]:
    '''Build checkpoints.'''

    if initial_item_count <= 0:
        raise ValueError("initial_item_count must be positive.")

    checkpoint_counts = set()

    i = 0

    while i <= 20:
        checkpoint_counts.add(round(initial_item_count * i / 20))
        i += 1

    return checkpoint_counts

def measure_attack_step(
    graph: nx.Graph,
    initial_node_count: int,
    removed_fraction: float,
    removed_count: int,
    is_path_metric_checkpoint: bool,
    removed_item: Hashable | None = None,
) -> AttackStep:
    '''Measure one attack step relative to the initial graph size.'''

    if initial_node_count <= 0:
        raise ValueError("initial_node_count must be positive.")

    start = time.perf_counter()

    component_sizes = compute_component_sizes(graph)

    component_count = len(component_sizes)

    if component_count >= 2:
        largest_component_size = component_sizes[0]
        second_largest_component_size = component_sizes[1]
        second_largest_component_ratio = second_largest_component_size / initial_node_count

    elif component_count == 1:
        largest_component_size = component_sizes[0]
        second_largest_component_size = 0
        second_largest_component_ratio = 0.0

    else :
        largest_component_size = 0
        second_largest_component_size = 0
        second_largest_component_ratio = 0.0

    if is_path_metric_checkpoint:
        diameter_lcc, average_shortest_path_length_lcc, global_efficiency = compute_shortest_path_metrics(graph)

    else:
        diameter_lcc = None
        average_shortest_path_length_lcc = None
        global_efficiency = None

    end = time.perf_counter()

    runtime_seconds = end - start

    step : AttackStep = {
            "removed_fraction": removed_fraction,
            "removed_count": removed_count,
            "remaining_nodes": graph.number_of_nodes(),
            "remaining_edges": graph.number_of_edges(),
            "component_count": component_count,
            "largest_component_size": largest_component_size,
            "largest_component_ratio": largest_component_size / initial_node_count,
            "second_largest_component_size": second_largest_component_size,
            "second_largest_component_ratio": second_largest_component_ratio,
            "removed_item": removed_item,
            "diameter_lcc": diameter_lcc,
            "average_shortest_path_length_lcc": average_shortest_path_length_lcc,
            "global_efficiency": global_efficiency,
            "runtime_seconds": runtime_seconds,
        }

    return step

def simulate_random_node_failure(
    graph: nx.Graph,
    seed: int,
) -> AttackHistory:
    '''Randomly remove nodes from a graph copy and record each attack step.'''

    initial_node_count = graph.number_of_nodes()
    working_graph = graph.copy()
    history : AttackHistory = []

    if initial_node_count == 0:
        return history

    checkpoint_counts = build_path_metric_checkpoints(initial_node_count)

    initial_step = measure_attack_step(working_graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=True)
    history.append(initial_step)

    rng = random.Random(seed)

    while working_graph.number_of_nodes() > 0:
        removed_node = rng.choice(list(working_graph.nodes))
        working_graph.remove_node(removed_node)

        removed_count = initial_node_count - working_graph.number_of_nodes()

        is_path_metric_checkpoint = removed_count in checkpoint_counts

        removed_fraction = removed_count / initial_node_count
        removed_item = removed_node

        step = measure_attack_step(working_graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint, removed_item)

        history.append(step)

    return history

def simulate_random_edge_failure(
    graph: nx.Graph,
    seed: int,
) -> AttackHistory:
    '''Randomly remove edges from a graph copy and record each attack step.'''

    initial_node_count = graph.number_of_nodes()
    initial_edge_count = graph.number_of_edges()
    working_graph = graph.copy()
    history: AttackHistory = []

    if initial_edge_count == 0:
        return history

    checkpoint_counts = build_path_metric_checkpoints(initial_edge_count)

    initial_step = measure_attack_step(working_graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=True)
    history.append(initial_step)

    rng = random.Random(seed)

    while working_graph.number_of_edges() > 0:
        removed_edge = rng.choice(list(working_graph.edges))
        working_graph.remove_edge(*removed_edge)

        removed_count = initial_edge_count - working_graph.number_of_edges()

        is_path_metric_checkpoint = removed_count in checkpoint_counts

        removed_fraction = removed_count / initial_edge_count
        removed_item = removed_edge

        step = measure_attack_step(working_graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint, removed_item)

        history.append(step)

    return history
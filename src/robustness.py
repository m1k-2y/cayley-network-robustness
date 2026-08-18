'''Simulate graph attacks and record robustness metrics at each step.'''
from typing import TypedDict
from collections.abc import Hashable
from src.metrics import compute_component_sizes
from src.metrics import compute_shortest_path_metrics
from src.metrics import compute_algebraic_connectivity
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
    algebraic_connectivity: float | None

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
        algebraic_connectivity = compute_algebraic_connectivity(graph)

    else:
        diameter_lcc = None
        average_shortest_path_length_lcc = None
        global_efficiency = None
        algebraic_connectivity = None

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
            "algebraic_connectivity": algebraic_connectivity,
        }

    return step

def simulate_random_node_failure(
    graph: nx.Graph,
    seed: int,
    max_removed_fraction: float = 1.0,
) -> AttackHistory:
    '''Randomly remove nodes from a graph copy and record each attack step.'''

    initial_node_count = graph.number_of_nodes()
    working_graph = graph.copy()
    history : AttackHistory = []

    if (max_removed_fraction < 0.0) or (max_removed_fraction > 1.0):
        raise ValueError("max_removed_fraction must be between 0.0 to 1.0.")

    if initial_node_count == 0:
        return history

    checkpoint_counts = build_path_metric_checkpoints(initial_node_count)

    initial_step = measure_attack_step(working_graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=True)
    history.append(initial_step)

    rng = random.Random(seed)

    max_removed_count = int(initial_node_count * max_removed_fraction)

    while initial_node_count - working_graph.number_of_nodes() < max_removed_count:
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
    max_removed_fraction: float = 1.0,
) -> AttackHistory:
    '''Randomly remove edges from a graph copy and record each attack step.'''

    initial_node_count = graph.number_of_nodes()
    initial_edge_count = graph.number_of_edges()
    working_graph = graph.copy()
    history: AttackHistory = []

    if max_removed_fraction < 0.0 or max_removed_fraction > 1.0:
        raise ValueError("max_removed_fraction must be between 0.0 to 1.0.")

    if initial_edge_count == 0:
        return history

    checkpoint_counts = build_path_metric_checkpoints(initial_edge_count)

    initial_step = measure_attack_step(working_graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=True)
    history.append(initial_step)

    rng = random.Random(seed)

    max_removed_count = int(initial_edge_count * max_removed_fraction)

    while initial_edge_count - working_graph.number_of_edges() < max_removed_count:
        removed_edge = rng.choice(list(working_graph.edges))
        working_graph.remove_edge(*removed_edge)

        removed_count = initial_edge_count - working_graph.number_of_edges()

        is_path_metric_checkpoint = removed_count in checkpoint_counts

        removed_fraction = removed_count / initial_edge_count
        removed_item = removed_edge

        step = measure_attack_step(working_graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint, removed_item)

        history.append(step)

    return history

def simulate_hop_localized_node_failure(
    graph: nx.Graph,
    seed: int,
    max_removed_fraction: float = 1.0,
) -> AttackHistory:
    '''Simulate hop-localized node failures on a connected graph.

    The removal order is determined before the attack using hop distance
    from a seed-selected start node in the original graph. Nodes at the
    same hop distance are shuffled reproducibly using the given seed.

    The input graph must be connected.
    '''
    
    working_graph = graph.copy()
    initial_node_count = graph.number_of_nodes()
    history: AttackHistory = []

    if max_removed_fraction < 0.0 or max_removed_fraction > 1.0:
        raise ValueError("max_removed_fraction must be between 0 to 1.")

    if initial_node_count == 0:
        return history

    if not nx.is_connected(graph):
        raise ValueError("graph must be connected.")

    checkpoint_counts = build_path_metric_checkpoints(initial_node_count)

    initial_step = measure_attack_step(working_graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=True)
    history.append(initial_step)

    rng = random.Random(seed)
    start_node = rng.choice(list(working_graph.nodes))

    path_length = nx.single_source_shortest_path_length(working_graph, start_node)
    length_dict = {}
    removal_order = []

    for node, length in path_length.items():
        if length in length_dict:
            length_dict[length].append(node)

        else:
            length_dict[length] = []
            length_dict[length].append(node)

    for key in sorted(length_dict):
        rng.shuffle(length_dict[key])

    for key in sorted(length_dict):
        for index in range(len(length_dict[key])):
            removal_order.append(length_dict[key][index])

    max_removed_count = int(initial_node_count * max_removed_fraction)

    removed_count = 0

    while initial_node_count - working_graph.number_of_nodes() < max_removed_count:
        removed_node = removal_order[removed_count]
        working_graph.remove_node(removed_node)

        removed_count += 1

        removed_fraction = removed_count / initial_node_count

        is_path_metric_checkpoint = removed_count in checkpoint_counts

        removed_item = removed_node

        step = measure_attack_step(working_graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint, removed_item)

        history.append(step)

    return history

def simulate_adaptive_betweenness_node_attack(
    graph: nx.Graph,
    seed: int, 
    max_removed_fraction: float = 1.0,
    k: int | None = None, 
) -> AttackHistory:

    working_graph = graph.copy()
    initial_node_count = graph.number_of_nodes()
    history: AttackHistory = []

    if max_removed_fraction < 0.0 or max_removed_fraction > 1.0:
        raise ValueError("max_removed_fraction must be between 0 to 1.")

    if k is not None:
        if k <= 0:
            raise ValueError("k must be bigger than 0.")

    if initial_node_count == 0:
        return history

    checkpoint_counts = build_path_metric_checkpoints(initial_node_count)


    initial_step = measure_attack_step(working_graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=True)
    history.append(initial_step)

    rng = random.Random(seed)

    max_removed_count = int(initial_node_count * max_removed_fraction)
    removed_count = 0

    while initial_node_count - working_graph.number_of_nodes() < max_removed_count:
        if k is None:
            effective_k = None

        else:
            if working_graph.number_of_nodes() < k:
                effective_k = working_graph.number_of_nodes()

            else:
                effective_k = k

        centrality = nx.betweenness_centrality(
            working_graph,
            k=effective_k,
            seed=seed,
        )

        max_value = 0.0
        max_value_node = []

        for _, betweenness in centrality.items():
            if betweenness > max_value:
                max_value = betweenness

        for node, betweenness in centrality.items():
            if abs(max_value - betweenness) < 1e-9:
                max_value_node.append(node)

        removed_item = rng.choice(max_value_node)

        working_graph.remove_node(removed_item)

        removed_count += 1

        removed_fraction = removed_count / initial_node_count

        is_path_metric_checkpoint = removed_count in checkpoint_counts

        step = measure_attack_step(working_graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint, removed_item)

        history.append(step)

    return history

def simulate_generator_class_edge_failure(
    graph: nx.Graph,
    seed: int,
    target_class: str,
    target_class_removal_fraction: float,
) -> AttackHistory:

    if target_class_removal_fraction < 0.0 or target_class_removal_fraction > 1.0:
        raise ValueError("target_class_removal_fraction must be between 0.0 to 1.0.")

    if target_class not in graph.graph["edge_classes"]:
        raise ValueError("Invalid target_class.")

    initial_node_count = graph.number_of_nodes()
    initial_edge_count = graph.number_of_edges()

    target_edges = []
    for (u, v, data) in graph.edges(data=True):
        if data["edge_class"] == target_class:
            target_edges.append((u, v))      

    working_graph = graph.copy()
    history: AttackHistory = []

    initial_step = measure_attack_step(working_graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=True)
    history.append(initial_step)

    checkpoint_counts = build_path_metric_checkpoints(initial_edge_count)

    rng = random.Random(seed)

    max_removed_count = int(target_class_removal_fraction * len(target_edges))
    removed_count = 0

    while removed_count < max_removed_count:
        removed_item = rng.choice(target_edges)

        working_graph.remove_edge(*removed_item)

        target_edges.remove(removed_item)

        removed_count += 1

        removed_fraction = removed_count / initial_edge_count

        is_path_metric_checkpoint = removed_count in checkpoint_counts

        step = measure_attack_step(working_graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint, removed_item)

        history.append(step)

    return history
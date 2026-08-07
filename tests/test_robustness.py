import networkx as nx
import pytest
from src.robustness import measure_attack_step
from src.robustness import simulate_random_node_failure
from src.robustness import build_path_metric_checkpoints

def test_measure_attack_step_connected_graph():

    graph = nx.path_graph(4)
    removed_fraction = 0.0
    initial_node_count = graph.number_of_nodes()

    step = measure_attack_step(graph, initial_node_count, removed_fraction, is_path_metric_checkpoint=True)

    assert step['removed_fraction'] == 0.0
    assert step['remaining_nodes'] == 4
    assert step['component_count'] == 1
    assert step['giant_component_size'] == 4
    assert step['giant_component_ratio'] == 1.0
    assert step["second_largest_component_ratio"] == 0.0
    assert step['removed_item'] is None
    assert step["diameter"] == 3
    assert step["average_shortest_path_length"] == pytest.approx(5 / 3)
    assert step["global_efficiency"] == pytest.approx(13/ 18)

def test_measure_attack_step_disconnected_graph():

    graph = nx.path_graph(6)

    initial_node_count = graph.number_of_nodes()
    graph.remove_node(3)
    removed_fraction = 1 / initial_node_count
    removed_item = 3

    step = measure_attack_step(graph, initial_node_count, removed_fraction, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == pytest.approx(1 / 6)
    assert step['remaining_nodes'] == 5
    assert step['component_count'] == 2
    assert step['giant_component_size'] == 3
    assert step['giant_component_ratio'] == 0.5
    assert step["second_largest_component_ratio"] == pytest.approx(1 / 3)
    assert step['removed_item'] == 3

def test_measure_attack_step_empty_graph():

    graph = nx.path_graph(4)

    initial_node_count = graph.number_of_nodes()
    graph.remove_nodes_from(list(graph.nodes))
    removed_fraction = 1.0
    removed_item = 3

    step = measure_attack_step(graph, initial_node_count, removed_fraction, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == 1.0
    assert step['remaining_nodes'] == 0
    assert step['component_count'] == 0
    assert step['giant_component_size'] == 0
    assert step['giant_component_ratio'] == 0.0
    assert step["second_largest_component_ratio"] == 0.0
    assert step['removed_item'] == removed_item

def test_measure_attack_step_single_node_graph():

    graph = nx.path_graph(4)
    initial_node_count = graph.number_of_nodes()

    for i in range(3):
        graph.remove_node(i)

    removed_fraction = 3 / initial_node_count
    removed_item = 2

    step = measure_attack_step(graph, initial_node_count, removed_fraction, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == removed_fraction
    assert step['remaining_nodes'] == 1
    assert step['component_count'] == 1
    assert step['giant_component_size'] == 1
    assert step['giant_component_ratio'] == 0.25
    assert step["second_largest_component_ratio"] == 0.0
    assert step['removed_item'] == removed_item

def test_simulate_random_node_failure_basic():

    graph = nx.path_graph(4)

    history = simulate_random_node_failure(graph)

    assert len(history) == 5
    assert history[len(history) - 1]['remaining_nodes'] == 0
    assert history[len(history) - 1]['removed_fraction'] == 1.0

    assert history[0]['remaining_nodes'] == 4
    assert history[0]['removed_fraction'] == 0.0
    assert history[0]['removed_item'] is None

    removed_items = []
    for step in history[1:]:
        removed_items.append(step['removed_item'])

    assert set(graph.nodes) == set(removed_items)

    assert graph.number_of_nodes() == 4

def test_build_path_metric_checkpoints_for_256_nodes():

    initial_node_count = 256

    checkpoint_count = build_path_metric_checkpoints(initial_node_count)

    assert 0 in checkpoint_count
    assert 13 in checkpoint_count
    assert 26 in checkpoint_count
    assert 256 in checkpoint_count

    assert len(checkpoint_count) == 21

def test_build_path_metric_checkpoints_rejects_nonpositive_node_count():

    initial_node_count = 0

    with pytest.raises(ValueError):
        build_path_metric_checkpoints(initial_node_count)

    initial_node_count = -1

    with pytest.raises(ValueError):
        build_path_metric_checkpoints(initial_node_count)

def test_measure_attack_step_skips_path_metrics_outside_checkpoint():

    graph = nx.path_graph(100)

    initial_node_count = graph.number_of_nodes()
    graph.remove_node(0)
    removed_fraction = 1 / initial_node_count
    removed_item = 0

    step = measure_attack_step(graph, initial_node_count, removed_fraction, is_path_metric_checkpoint=False, removed_item=removed_item)

    assert step["removed_fraction"] == removed_fraction
    assert step["remaining_nodes"] == 99
    assert step["component_count"] == 1
    assert step["giant_component_size"] == 99
    assert step["giant_component_ratio"] == 0.99
    assert step["removed_item"] == removed_item
    assert step["diameter"] is None
    assert step["average_shortest_path_length"] is None
    assert step["global_efficiency"] is None

def test_simulate_random_node_failure_uses_path_metric_checkpoints():

    graph = nx.path_graph(100)

    history = simulate_random_node_failure(graph)

    assert history[1]['diameter'] is None
    assert history[1]['average_shortest_path_length'] is None
    assert history[1]['global_efficiency'] is None

    assert history[5]['diameter'] is not None
    assert history[5]['average_shortest_path_length'] is not None
    assert history[5]['global_efficiency'] is not None
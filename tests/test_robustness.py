import networkx as nx
import pytest
from src.robustness import measure_attack_step
from src.robustness import simulate_random_node_failure
from src.robustness import build_path_metric_checkpoints
from src.robustness import simulate_random_edge_failure
from src.robustness import build_experiment_row
from src.cayley_graph import create_cyclic_cayley_graph

def test_measure_attack_step_connected_graph():

    graph = nx.path_graph(4)
    removed_fraction = 0.0
    removed_count = 0
    initial_node_count = graph.number_of_nodes()

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=True)

    assert step['removed_fraction'] == 0.0
    assert step['removed_count'] == 0
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
    removed_count = 1
    removed_item = 3

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == pytest.approx(1 / 6)
    assert step['removed_count'] == 1
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
    removed_count = 4
    removed_item = 3

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == 1.0
    assert step['removed_count'] == 4
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
    removed_count = 3
    removed_item = 2

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == removed_fraction
    assert step['removed_count'] == 3
    assert step['remaining_nodes'] == 1
    assert step['component_count'] == 1
    assert step['giant_component_size'] == 1
    assert step['giant_component_ratio'] == 0.25
    assert step["second_largest_component_ratio"] == 0.0
    assert step['removed_item'] == removed_item

def test_simulate_random_node_failure_basic():

    graph = nx.path_graph(4)

    history = simulate_random_node_failure(graph, seed=42)

    assert len(history) == 5
    assert history[len(history) - 1]['remaining_nodes'] == 0
    assert history[len(history) - 1]['removed_fraction'] == 1.0
    assert history[len(history) - 1]['removed_count'] == 4

    assert history[0]['remaining_nodes'] == 4
    assert history[0]['removed_fraction'] == 0.0
    assert history[0]['removed_count'] == 0
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
    removed_count = 1
    removed_item = 0

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=False, removed_item=removed_item)

    assert step["removed_fraction"] == removed_fraction
    assert step['removed_count'] == removed_count
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

    history = simulate_random_node_failure(graph, seed=42)

    assert history[1]['diameter'] is None
    assert history[1]['average_shortest_path_length'] is None
    assert history[1]['global_efficiency'] is None

    assert history[5]['diameter'] is not None
    assert history[5]['average_shortest_path_length'] is not None
    assert history[5]['global_efficiency'] is not None

def test_simulate_random_edge_failure_basic():

    graph = nx.path_graph(4)

    history = simulate_random_edge_failure(graph, seed=42)

    assert len(history) == 4

    assert history[0]["removed_fraction"] == 0.0
    assert history[0]['removed_count'] == 0
    assert history[0]["removed_item"] is None

    assert history[len(history) - 1]["removed_fraction"] == 1.0
    assert history[len(history) - 1]['removed_count'] == 3
    assert history[len(history) - 1]["remaining_nodes"] == 4

    edges = set()
    for step in history[1:]:
        edges.add(step["removed_item"])

    assert set(graph.edges) == edges

def test_simulate_random_edge_failure_uses_path_metric_checkpoints():

    graph = nx.path_graph(100)

    history = simulate_random_edge_failure(graph, seed=42)

    assert history[1]["diameter"] is None
    assert history[1]["average_shortest_path_length"] is None
    assert history[1]["global_efficiency"] is None

    assert history[5]["diameter"] is not None
    assert history[5]["average_shortest_path_length"] is not None
    assert history[5]["global_efficiency"] is not None

def test_random_node_failure_is_reproducible_with_same_seed():

    graph = nx.path_graph(4)
    seed = 42

    history1 = simulate_random_node_failure(graph, seed)
    history2 = simulate_random_node_failure(graph, seed)

    for i in range(5):
        assert history1[i]["removed_item"] == history2[i]["removed_item"]

def test_random_edge_failure_is_reproducible_with_same_seed():

    graph = nx.path_graph(4)
    seed = 42

    history1 = simulate_random_edge_failure(graph, seed)
    history2 = simulate_random_edge_failure(graph, seed)

    for i in range(4):
        assert history1[i]["removed_item"] == history2[i]["removed_item"]

def test_build_experiment_row_combines_metadata_and_attack_step():

    n = 4
    generators = {1, -1}

    graph = create_cyclic_cayley_graph(n, generators)

    initial_node_count = 4

    step = measure_attack_step(graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=False)

    graph_family = "cyclic_local"
    attack_type = "random"
    attack_seed = 42
    removal_type = "node"

    row = build_experiment_row(graph_family=graph_family, n=n, graph_seed=None, attack_type=attack_type, attack_seed=attack_seed, removal_type=removal_type, step=step)

    assert row["graph_family"] == graph_family
    assert row["n"] == n
    assert row["graph_seed"] is None
    assert row["attack_type"] == attack_type
    assert row["attack_seed"] == attack_seed
    assert row["removal_type"] == removal_type

    assert row["removed_count"] == step["removed_count"]
    assert row['removed_fraction'] == step["removed_fraction"]
    assert row["giant_component_ratio"] == step["giant_component_ratio"]

    assert row["diameter"] is None
    assert row["average_shortest_path_length"] is None
    assert row["global_efficiency"] is None
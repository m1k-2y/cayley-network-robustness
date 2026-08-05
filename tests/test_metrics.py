from src.metrics import compute_basic_metrics
from src.cayley_graph import create_cyclic_cayley_graph
from src.metrics import compute_component_metrics
import networkx as nx
import pytest

def test_compute_basic_metrics_for_connected_cyclic_cayley_graph():

    n = 5
    generators = {1, -1}

    graph = create_cyclic_cayley_graph(n, generators)

    metrics = compute_basic_metrics(graph)

    assert metrics["num_nodes"] == 5
    assert metrics["num_edges"] == 5
    assert metrics["is_connected"]
    assert metrics["num_components"] == 1
    assert metrics["average_degree"] == 2.0
    assert metrics["diameter"] == 2
    assert metrics["giant_component_ratio"] == 1.0
    assert metrics["average_shortest_path_length"] == 1.5

def test_compute_basic_metrics_for_empty_graph():

    graph = nx.Graph()

    metrics = compute_basic_metrics(graph)

    assert metrics["num_nodes"] == 0
    assert metrics["num_edges"] == 0
    assert not metrics["is_connected"] 
    assert metrics["num_components"] == 0
    assert metrics["average_degree"] == 0.0
    assert metrics["diameter"] is None
    assert metrics["giant_component_ratio"] == 0.0
    assert metrics["average_shortest_path_length"] is None

def test_compute_basic_metrics_for_disconnected_cyclic_cayley_graph():

    n = 8
    generators = {2, -2}

    graph = create_cyclic_cayley_graph(n, generators)

    metrics = compute_basic_metrics(graph)

    assert metrics["num_nodes"] == 8
    assert metrics["num_edges"] == 8
    assert not metrics["is_connected"]
    assert metrics["num_components"] == 2
    assert metrics["average_degree"] == 2.0
    assert metrics["diameter"] is None
    assert metrics["giant_component_ratio"] == 0.5
    assert metrics["average_shortest_path_length"] is None

def test_compute_component_metrics_for_connected_graph():

    graph = nx.path_graph(6)
    initial_node_count = 6

    component_metrics = compute_component_metrics(graph, initial_node_count)

    expected_metrics = {
        "remaining_nodes": 6,
        "component_count": 1,
        "s1": 1.0,
        "s2": 0.0,
    }

    assert component_metrics == expected_metrics

def test_compute_component_metrics_uses_initial_node_count():

    graph = nx.path_graph(6)
    initial_node_count = 6

    graph.remove_node(5)
    graph.remove_node(4)

    component_metrics = compute_component_metrics(graph, initial_node_count)

    expected_metrics = {
        "remaining_nodes": 4,
        "component_count": 1,
        "s1": 4 / 6,
        "s2": 0.0,
    }

    assert component_metrics == expected_metrics

def test_compute_component_metrics_for_empty_graph():

    graph = nx.Graph()
    initial_node_count = 6

    component_metrics = compute_component_metrics(graph, initial_node_count)

    expected_metrics = {
        "remaining_nodes": 0,
        "component_count": 0,
        "s1": 0.0,
        "s2": 0.0,
    }

    assert component_metrics == expected_metrics

def test_compute_component_metrics_for_two_components():

    graph = nx.path_graph(6)
    initial_node_count = 6

    graph.remove_node(3)

    component_metrics = compute_component_metrics(graph, initial_node_count)

    expected_metrics = {
        "remaining_nodes": 5,
        "component_count": 2,
        "s1": 3 / 6,
        "s2": 2 / 6,
    }

    assert component_metrics == expected_metrics

def test_compute_component_metrics_selects_two_largest_components():

    graph = nx.path_graph(11)
    initial_node_count = 11

    graph.remove_node(4)
    graph.remove_node(8)

    component_metrics = compute_component_metrics(graph, initial_node_count)

    expected_metrics = {
        "remaining_nodes": 9,
        "component_count": 3,
        "s1": 4 / 11,
        "s2": 3 / 11,
    }

    assert component_metrics == expected_metrics

def test_compute_component_metrics_rejects_nonpositive_initial_node_count():

    graph = nx.path_graph(6)

    initial_node_count = 0
    with pytest.raises(ValueError):
        compute_component_metrics(graph, initial_node_count)

    initial_node_count = -1
    with pytest.raises(ValueError):
        compute_component_metrics(graph, initial_node_count)
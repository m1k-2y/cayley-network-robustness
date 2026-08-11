from src.metrics import compute_basic_metrics
from src.cayley_graph import create_cyclic_cayley_graph
from src.metrics import get_largest_connected_component
from src.metrics import compute_diameter
from src.metrics import compute_average_shortest_path_length
from src.metrics import compute_global_efficiency
from src.metrics import compute_algebraic_connectivity
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
    assert metrics["global_efficiency"] == pytest.approx(3 / 4)

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
    assert metrics["global_efficiency"] == 0.0

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
    assert metrics["diameter"] == 2
    assert metrics["giant_component_ratio"] == 0.5
    assert metrics["average_shortest_path_length"] == pytest.approx(4 / 3)
    assert metrics["global_efficiency"] == pytest.approx(5 / 14)

def test_get_largest_connected_component_returns_none_for_empty_graph():

    graph = nx.Graph()

    test_graph = get_largest_connected_component(graph)

    assert test_graph is None

def test_get_largest_connected_component_for_connected_graph():

    graph = nx.path_graph(6)

    test_graph = get_largest_connected_component(graph)

    assert test_graph is not None
    assert set(graph.nodes()) == set(test_graph.nodes())
    assert set(graph.edges()) == set(test_graph.edges())

def test_get_largest_connected_component_selects_largest():

    graph = nx.path_graph(8)
    graph.remove_node(3)

    largest_component = get_largest_connected_component(graph)

    expected_nodes_set = {4, 5, 6, 7}
    expected_edges_set = {
        (4, 5),
        (5, 6),
        (6, 7),
    }

    assert largest_component is not None
    assert set(largest_component.nodes()) == expected_nodes_set
    assert set(largest_component.edges()) == expected_edges_set

def test_get_largest_connected_component_breaks_tie_by_smallest_node():

    graph = nx.Graph()

    graph.add_edges_from([
        (10, 11),
        (10, 12),
        (10, 13),
    ])

    graph.add_edges_from([
        (0, 1),
        (1, 2),
        (2, 3),
    ])

    largest_component = get_largest_connected_component(graph)

    expected_nodes_set = {0, 1, 2, 3}

    assert largest_component is not None
    assert set(largest_component.nodes()) == expected_nodes_set

def test_compute_diameter_uses_largest_connected_component():

    graph = nx.path_graph(8)

    graph.remove_node(3)

    diameter = compute_diameter(graph)

    assert diameter == 3

def test_compute_average_shortest_path_length_uses_largest_connected_component():

    graph = nx.path_graph(8)

    graph.remove_node(3)

    average_length  = compute_average_shortest_path_length(graph)

    assert average_length == 5 / 3

def test_compute_global_efficiency_for_empty_graph():

    graph = nx.Graph()

    global_efficiency = compute_global_efficiency(graph)

    assert global_efficiency == 0.0

def test_compute_global_efficiency_for_single_node():

    graph = nx.path_graph(1)

    global_efficiency = compute_global_efficiency(graph)

    assert global_efficiency == 0.0

def test_compute_global_efficiency_for_connected_graph():

    graph = nx.path_graph(3)

    global_efficiency = compute_global_efficiency(graph)

    assert global_efficiency == pytest.approx(5 / 6)

def test_compute_global_efficiency_for_disconnected_graph():

    graph = nx.path_graph(3)
    graph.add_node(3)

    global_efficiency = compute_global_efficiency(graph)

    assert global_efficiency == pytest.approx(5 / 12)

def test_compute_algebraic_connectivity_empty_graph():

    graph = nx.path_graph(0)

    assert compute_algebraic_connectivity(graph) == 0.0

def test_compute_algebraic_connectivity_single_node():

    graph = nx.path_graph(1)

    assert compute_algebraic_connectivity(graph) == 0.0

def test_compute_algebraic_connectivity_disconnected_graph():

    graph = nx.path_graph(3)
    graph.add_node(3)

    assert compute_algebraic_connectivity(graph) == 0.0

def test_compute_algebraic_connectivity_connected_graph():

    graph = nx.path_graph(3)

    assert compute_algebraic_connectivity(graph) == pytest.approx(1.0)
from src.metrics import compute_basic_metrics
from src.cayley_graph import create_cyclic_cayley_graph
import networkx as nx

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
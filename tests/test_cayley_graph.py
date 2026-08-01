import networkx as nx
from src.cayley_graph import create_cyclic_cayley_graph
import pytest
from src.cayley_graph import draw_graph
from src.metrics import compute_basic_metrics

def test_rejects_zero_n():
    
    n = 0
    generators = {1}

    with pytest.raises(ValueError):
        create_cyclic_cayley_graph(n, generators)

def test_rejects_negative_n():

    n = -1
    generators = {1}

    with pytest.raises(ValueError):
        create_cyclic_cayley_graph(n, generators)

def test_rejects_self_loop():

    n = 5
    generators = {0}

    with pytest.raises(ValueError):
        create_cyclic_cayley_graph(n, generators)

def test_rejects_generator_congruent_to_zero():

    n = 5
    generators = {5}

    with pytest.raises(ValueError):
        create_cyclic_cayley_graph(n, generators)

def test_normalizes_generators_modulo_n():

    n = 5
    generators1 = {1}
    generators2 = {6}

    graph1 = create_cyclic_cayley_graph(n, generators1)
    graph2 = create_cyclic_cayley_graph(n, generators2)

    assert graph1.adj == graph2.adj

def test_allows_empty_generators():

    n = 5
    generators = set()

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 0

def test_allows_single_vertex_with_empty_generators():

    n = 1
    generators = set()

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 1
    assert graph.number_of_edges() == 0

def test_draw_graph_rejects_invalid_layout():

    n = 5
    generators = {1, -1}

    graph = create_cyclic_cayley_graph(n, generators)

    with pytest.raises(ValueError):
        draw_graph(graph, "invalid", "invalid_layout.png")

def test_z5_with_plus_minus_one():
    
    n = 5
    generators = {1, -1}

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 5

    for node, degree in graph.degree():
        assert degree == 2
    
    assert nx.is_connected(graph)

def test_z8_with_plus_minus_two():
    
    n = 8
    generators = {2, -2}

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 8
    assert graph.number_of_edges() == 8

    for node, degree in graph.degree():
        assert degree == 2
    
    assert not nx.is_connected(graph)

    assert nx.number_connected_components(graph) == 2

def test_cyclic_cayley_graph_edge_class_step_1():

    n = 8
    generators = {-1, 1}

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 8
    assert graph.number_of_edges() == 8
    
    for _, degree in graph.degree():
        assert degree == 2

    assert nx.is_connected(graph)

    for u, v in graph.edges():
        assert graph.edges[u, v]["edge_class"] == "step_1"

    assert graph.graph["family"] == "cyclic"
    assert graph.graph["generators"] == (-1, 1)
    assert graph.graph["edge_classes"] == ("step_1",)

def test_cyclic_cayley_graph_involution():

    n = 8
    generators = {4}

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 8
    assert graph.number_of_edges() == 4

    for _, degree in graph.degree():
        assert degree == 1
    
    assert not nx.is_connected(graph)
    
    for u, v in graph.edges():
        assert graph.edges[u, v]["edge_class"] == "step_4"
    
    assert graph.graph["family"] == "cyclic"
    assert graph.graph["generators"] == (4,)
    assert graph.graph["edge_classes"] == ("step_4",)

def test_cyclic_cayley_graph_multiple_edge_classes():

    n = 256
    generators = {1, -1, 2, -2}

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 256
    assert graph.number_of_edges() == 512

    for _, degree in graph.degree():
        assert degree == 4
    
    assert nx.is_connected(graph)

    for u, v in graph.edges():
        assert graph.edges[u, v]["edge_class"] in {"step_1", "step_2"}
    
    assert graph.graph["family"] == "cyclic"
    assert graph.graph["generators"] == (-2, -1, 1, 2)
    assert graph.graph["edge_classes"] == ("step_1", "step_2")

def test_cyclic_cayley_graph_long_jump_edge_classes():

    n = 256
    generators = {1, -1, 64, -64}

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 256
    assert graph.number_of_edges() == 512

    for _, degree in graph.degree():
        assert degree == 4
    
    assert nx.is_connected(graph)

    for u, v in graph.edges():
        assert graph.edges[u, v]["edge_class"] in {"step_1", "step_64"}
    
    assert graph.graph["family"] == "cyclic"
    assert graph.graph["generators"] == (-64, -1, 1, 64)
    assert graph.graph["edge_classes"] == ("step_1", "step_64")

def test_cyclic_cayley_graph_edge_class_counts_sum_to_total():

    n = 256
    generators = {1, -1, 64, -64}

    graph = create_cyclic_cayley_graph(n, generators)

    s1 = 0
    s2 = 0

    for _, _, data in graph.edges(data = True):
        if data["edge_class"] == "step_1":
            s1 += 1
        
        elif data["edge_class"] == "step_64":
            s2 += 1
    
    assert s1 == 256
    assert s2 == 256
    assert s1 + s2 == graph.number_of_edges()

def test_cyclic_cayley_graph_equivalent_generator_representations():

    n = 256
    generators1 = {1, -1}
    generators2 = {1, 255}

    graph1 = create_cyclic_cayley_graph(n, generators1)
    graph2 = create_cyclic_cayley_graph(n, generators2)

    assert graph1.adj == graph2.adj

    assert graph1.graph["edge_classes"] == ("step_1",)
    assert graph2.graph["edge_classes"] == ("step_1",)
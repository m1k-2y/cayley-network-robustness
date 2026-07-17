import networkx as nx
from src.cayley_graph import create_cyclic_cayley_graph
import pytest
from src.cayley_graph import draw_graph

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

    assert nx.utils.graphs_equal(graph1, graph2)

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
import networkx as nx
from src.cayley_graph import create_cyclic_cayley_graph

def test_z5_with_plus_minus_one() :
    
    n = 5
    generators = {1, -1}

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 5

    for node, degree in graph.degree() :
        assert degree == 2
    
    assert nx.is_connected(graph)

def test_z8_with_plus_minus_two() :
    
    n = 8
    generators = {2, -2}

    graph = create_cyclic_cayley_graph(n, generators)

    assert graph.number_of_nodes() == 8
    assert graph.number_of_edges() == 8

    for node, degree in graph.degree() :
        assert degree == 2
    
    assert not nx.is_connected(graph)

    assert nx.number_connected_components(graph) == 2
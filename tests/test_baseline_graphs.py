from src.baseline_graphs import create_erdos_renyi_graph
import networkx as nx
import pytest

def test_erdos_renyi_graph_has_no_edges_when_p_is_zero():

    n = 5
    p = 0

    graph = create_erdos_renyi_graph(n, p)

    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 0

def test_erdos_renyi_graph_is_complete_when_p_is_one():

    n = 5
    p = 1

    graph = create_erdos_renyi_graph(n, p)

    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 10

def test_erdos_renyi_graph_is_reproducible_with_same_seed():

    n = 5
    p = 0.3
    seed = 42

    graph1 = create_erdos_renyi_graph(n, p, seed)
    graph2 = create_erdos_renyi_graph(n, p, seed)

    assert set(graph1.edges()) == set(graph2.edges())

def test_erdos_renyi_graph_rejects_non_positive_n():

    n = 0
    p = 0.3

    with pytest.raises(ValueError):
        create_erdos_renyi_graph(n, p)

def test_erdos_renyi_graph_rejects_p_outside_valid_range():

    n = 5

    p1 = -0.1
    p2 = 1.1

    with pytest.raises(ValueError):
        create_erdos_renyi_graph(n, p1)
    
    with pytest.raises(ValueError):
        create_erdos_renyi_graph(n, p2)
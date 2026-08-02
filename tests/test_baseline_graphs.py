from src.baseline_graphs import create_erdos_renyi_graph
import networkx as nx
import pytest
from src.baseline_graphs import create_barabasi_albert_graph
from src.baseline_graphs import create_watts_strogatz_graph
from src.baseline_graphs import create_random_regular_graph
from src.baseline_graphs import create_torus_2d_graph

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

def test_barabasi_albert_graph_has_expected_nodes_and_edges():

    n = 5
    m = 2
    seed = 42

    graph = create_barabasi_albert_graph(n, m, seed)

    assert graph.number_of_nodes() == 5
    assert graph.number_of_edges() == 6

def test_barabasi_albert_graph_is_reproducible_with_same_seed():

    n = 5
    m = 2
    seed = 42

    graph1 = create_barabasi_albert_graph(n, m, seed)
    graph2 = create_barabasi_albert_graph(n, m, seed)

    assert set(graph1.edges()) == set(graph2.edges())

def test_barabasi_albert_graph_rejects_non_positive_n():

    n = 0
    m = 1

    with pytest.raises(ValueError):
        create_barabasi_albert_graph(n, m)

def test_barabasi_albert_graph_rejects_non_positive_m():

    n = 5
    m = 0

    with pytest.raises(ValueError):
        create_barabasi_albert_graph(n, m)

def test_barabasi_albert_graph_rejects_m_not_smaller_than_n():

    n = 5
    m = 5

    with pytest.raises(ValueError):
        create_barabasi_albert_graph(n, m)

def test_watts_strogatz_graph_has_expected_nodes_and_edges():

    n = 10
    k = 4
    p = 0

    graph = create_watts_strogatz_graph(n, k, p)

    assert graph.number_of_nodes() == 10
    assert graph.number_of_edges() == 20

def test_watts_strogatz_graph_same_seed_is_reproducible():

    n = 20
    k = 4
    p = 0.3
    seed = 42

    graph1 = create_watts_strogatz_graph(n, k, p, seed)
    graph2 = create_watts_strogatz_graph(n, k, p, seed)

    assert set(graph1.edges()) == set(graph2.edges())

def test_watts_strogatz_graph_rejects_non_positive_n():

    n = 0
    k = 4
    p = 0.4

    with pytest.raises(ValueError):
        create_watts_strogatz_graph(n, k, p)

def test_watts_strogatz_graph_rejects_invalid_k_range():

    n = 10
    k = 0
    p = 0.4

    with pytest.raises(ValueError):
        create_watts_strogatz_graph(n, k, p)

def test_watts_strogatz_graph_rejects_odd_k():

    n = 10
    k = 3
    p = 0.4

    with pytest.raises(ValueError):
        create_watts_strogatz_graph(n, k, p)

def test_watts_strogatz_graph_rejects_invalid_probability():

    n = 10
    k = 4
    p = 1.1

    with pytest.raises(ValueError):
        create_watts_strogatz_graph(n, k, p)

def test_random_regular_graph_has_expected_nodes_edges_and_degrees():

    n = 10
    d = 4

    graph = create_random_regular_graph(n, d)

    assert graph.number_of_nodes() == 10
    assert graph.number_of_edges() == 20
    
    for _, degree in graph.degree():
        assert degree == 4

def test_random_regular_graph_is_reproducible_with_same_seed():

    n = 10
    d = 4
    seed = 42

    graph1 = create_random_regular_graph(n, d, seed)
    graph2 = create_random_regular_graph(n, d, seed)

    assert set(graph1.edges()) == set(graph2.edges())

def test_random_regular_graph_rejects_non_positive_n():

    n = -1
    d = 4

    with pytest.raises(ValueError):
        create_random_regular_graph(n, d)

def test_random_regular_graph_rejects_invalid_degree_range():

    n = 10
    d = -1

    with pytest.raises(ValueError):
        create_random_regular_graph(n, d)

def test_random_regular_graph_rejects_odd_degree_sum():

    n = 11
    d  = 5

    with pytest.raises(ValueError):
        create_random_regular_graph(n, d)

def test_create_2d_torus_graph_3x3_basic_properties():

    rows = 3
    cols = 3

    graph = create_torus_2d_graph(rows, cols)

    assert graph.number_of_nodes() == 9
    assert graph.number_of_edges() == 18

    for _, degree in graph.degree():
        assert degree == 4
    
    assert nx.is_connected(graph)

def test_create_2d_torus_graph_16x16_size_and_degree():

    rows = 16
    cols = 16

    graph = create_torus_2d_graph(rows, cols)

    assert graph.number_of_nodes() == 256
    assert graph.number_of_edges() == 512

    for _, degree in graph.degree():
        assert degree == 4

def test_create_2d_torus_graph_16x16_edge_class_counts():

    rows = 16
    cols = 16

    graph = create_torus_2d_graph(rows, cols)

    h = 0
    v = 0

    for _, _, data in graph.edges(data = True):
        if data["edge_class"] == "horizontal":
            h += 1
        
        elif data["edge_class"] == "vertical":
            v += 1
    
    assert h == 256
    assert v == 256

    assert h + v == graph.number_of_edges()

def test_create_2d_torus_graph_16x16_diameter():

    rows = 16
    cols = 16

    graph = create_torus_2d_graph(rows, cols)

    assert nx.diameter(graph) == 16

def test_create_2d_torus_graph_rejects_dimensions_below_3():

    rows1 = 2
    cols1 = 3

    with pytest.raises(ValueError):
        create_torus_2d_graph(rows1, cols1)
    
    rows2 = 3
    cols2 = 2

    with pytest.raises(ValueError):
        create_torus_2d_graph(rows2, cols2)
    
    rows3 = 1
    cols3 = 3

    with pytest.raises(ValueError):
        create_torus_2d_graph(rows3, cols3)

def test_create_2d_torus_graph_16x16_node_zero_neighbors():

    rows = 16
    cols = 16

    graph = create_torus_2d_graph(rows, cols)

    assert set(graph.neighbors(0)) == {1, 15, 16, 240}

def test_create_2d_torus_graph_removing_horizontal_edges_creates_16_components():

    rows = 16
    cols = 16

    graph = create_torus_2d_graph(rows, cols)

    horizontal_edges = []

    for u, v, data in graph.edges(data = True):
        if data["edge_class"] == "horizontal":
            horizontal_edges.append((u, v))
    
    graph.remove_edges_from(horizontal_edges)

    assert nx.number_connected_components(graph) == 16
from src.baseline_graphs import create_erdos_renyi_graph
import networkx as nx
import pytest
from src.baseline_graphs import create_barabasi_albert_graph
from src.baseline_graphs import create_watts_strogatz_graph
from src.baseline_graphs import create_random_regular_graph
from src.baseline_graphs import create_2d_lattice_graph

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

def test_2d_lattice_graph_has_expected_nodes_and_edges():

    rows = 3
    cols = 4

    graph = create_2d_lattice_graph(rows, cols)

    assert graph.number_of_nodes() == 12
    assert graph.number_of_edges() == 17

def test_2d_lattice_graph_has_expected_node_coordinates():

    rows = 3
    cols = 4

    nodes = set()

    graph = create_2d_lattice_graph(rows, cols)

    for x in range(rows):
        for y in range(cols):
            nodes.add((x, y))

    assert nodes == set(graph.nodes())

def test_2d_lattice_graph_has_expected_node_degrees():

    rows = 3
    cols = 4

    graph = create_2d_lattice_graph(rows, cols)

    assert graph.degree((0, 0)) == 2
    assert graph.degree((0, 1)) == 3
    assert graph.degree((1, 1)) == 4

def test_2d_lattice_graph_rejects_non_positive_rows():

    rows = -1
    cols = 4

    with pytest.raises(ValueError):
        create_2d_lattice_graph(rows, cols)

def test_2d_lattice_graph_rejects_non_positive_cols():

    rows = 3
    cols = -1

    with pytest.raises(ValueError):
        create_2d_lattice_graph(rows, cols)
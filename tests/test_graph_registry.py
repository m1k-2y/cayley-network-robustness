from src.graph_registry import build_graph
from src.graph_registry import SUPPORTED_GRAPH_NAMES
from src.graph_registry import SUPPORTED_NODE_COUNTS
import pytest
import networkx as nx

def test_build_graph_creates_all_supported_families_at_256():

    n = 256
    seed = 42

    supported_graph_names = {
        "cyclic_local",
        "cyclic_long_jump",
        "torus_2d",
        "random_regular",
        "watts_strogatz",
    }

    for name in supported_graph_names:
        graph = build_graph(name, n, seed)

        assert graph.number_of_nodes() == n
        assert graph.number_of_edges() == 2 * n
        assert graph.graph["family"] == name
        assert graph.graph["n"] == n
        assert "stochastic" in graph.graph
        assert "seed" in graph.graph
        assert "edge_classes" in graph.graph

def test_build_graph_creates_all_supported_families_at_1024():

    n = 1024
    seed = 42

    supported_graph_names = {
        "cyclic_local",
        "cyclic_long_jump",
        "torus_2d",
        "random_regular",
        "watts_strogatz",
    }

    for name in supported_graph_names:
        graph = build_graph(name, n, seed)

        assert graph.number_of_nodes() == n
        assert graph.number_of_edges() == 2 * n
        assert graph.graph["family"] == name
        assert graph.graph["n"] == n
        assert "stochastic" in graph.graph
        assert "seed" in graph.graph
        assert "edge_classes" in graph.graph

def test_stochastic_graphs_are_reproducible_with_same_seed():

    name = "random_regular"
    n = 256
    seed = 42

    graph1 = build_graph(name, n, seed)
    graph2 = build_graph(name, n, seed)

    assert graph1.adj == graph2.adj
    assert graph1.graph["stochastic"]
    assert graph1.graph["seed"] == 42

    name = "random_regular"
    n = 1024
    seed = 42
    
    graph1 = build_graph(name, n, seed)
    graph2 = build_graph(name, n, seed)
    
    assert graph1.adj == graph2.adj
    assert graph1.graph["stochastic"]
    assert graph1.graph["seed"] == 42

    name = "watts_strogatz"
    n = 256
    seed = 42
    
    graph1 = build_graph(name, n, seed)
    graph2 = build_graph(name, n, seed)
    
    assert graph1.adj == graph2.adj
    assert graph1.graph["stochastic"]
    assert graph1.graph["seed"] == 42
    
    name = "watts_strogatz"
    n = 1024
    seed = 42
        
    graph1 = build_graph(name, n, seed)
    graph2 = build_graph(name, n, seed)
        
    assert graph1.adj == graph2.adj
    assert graph1.graph["stochastic"]
    assert graph1.graph["seed"] == 42

def test_deterministic_graphs_ignore_seed():

    test_graph = {
        "cyclic_local",
        "cyclic_long_jump",
        "torus_2d"
    }

    for name in test_graph:
        graph1 = build_graph(name, 256, seed = 42)
        graph2 = build_graph(name, 256, seed = 999)

        assert graph1.adj == graph2.adj
        assert graph1.graph["stochastic"] is False
        assert graph2.graph["stochastic"] is False
        assert graph1.graph["seed"] is None
        assert graph2.graph["seed"] is None

def test_build_graph_rejects_unknown_name():

    name = "unknown_graph"
    n = 256

    with pytest.raises(ValueError):
        build_graph(name, n)

def test_build_graph_rejects_unsupported_node_count():

    name = "cyclic_local"

    unsupported_node_counts = {
        128,
        512,
    }

    for n in unsupported_node_counts:
        with pytest.raises(ValueError):
            build_graph(name, n)

def test_regular_families_have_degree_four():

    test_graph = {
        "cyclic_local",
        "cyclic_long_jump",
        "torus_2d",
        "random_regular",
    }

    n = 256
    seed = 42

    for name in test_graph:
        graph = build_graph(name, n, seed)
        for _, degree in graph.degree():
            assert degree == 4

def test_torus_2d_uses_expected_square_dimensions():

    test_node_count = {
        256 : 16,
        1024 : 32,
    }

    for n, side in test_node_count.items():
        graph = build_graph("torus_2d", n)
        assert graph.graph["rows"] == side
        assert graph.graph["cols"] == side

def test_cyclic_long_jump_uses_expected_edge_classes():

    test_node_count = {
        256: ("step_1", "step_64"),
        1024: ("step_1", "step_256"), 
    }

    for n, expected_edge_classes in test_node_count.items():
        graph = build_graph("cyclic_long_jump", n)
        assert graph.graph["edge_classes"] == expected_edge_classes

def test_non_structural_families_have_no_edge_classes():

    test_graph = {
        "random_regular",
        "watts_strogatz",
    }

    n = 256
    seed = 42

    for name in test_graph:
        graph = build_graph(name, n, seed)
        assert graph.graph["edge_classes"] == ()

def test_supported_graph_families_are_connected():

    for graph_name in SUPPORTED_GRAPH_NAMES:
        for n in SUPPORTED_NODE_COUNTS:
            graph = build_graph(
                name=graph_name,
                n=n,
                seed=42,
            )

            assert nx.is_connected(graph)

def test_stochastic_graphs_require_seed():

    with pytest.raises(ValueError):
        build_graph(
            name="random_regular",
            n=256,
        )

    with pytest.raises(ValueError):
        build_graph(
            name="watts_strogatz",
            n=256,
        )
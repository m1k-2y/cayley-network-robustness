import networkx as nx
import math
from src.cayley_graph import create_cyclic_cayley_graph
from src.baseline_graphs import create_torus_2d_graph
from src.baseline_graphs import create_random_regular_graph
from src.baseline_graphs import create_watts_strogatz_graph

SUPPORTED_GRAPH_NAMES = {
    "cyclic_local",
    "cyclic_long_jump",
    "torus_2d",
    "random_regular",
    "watts_strogatz",
}

SUPPORTED_NODE_COUNTS = {
    256,
    1024,
}

def build_graph(
    name: str,
    n: int,
    seed: int | None = None,
) -> nx.Graph:

    if name not in SUPPORTED_GRAPH_NAMES:
        raise ValueError("name must be in SUPPORTED_GRAPH_NAMES")

    if n not in SUPPORTED_NODE_COUNTS:
        raise ValueError("n must be in SUPPORTED_NODE_COUNTS")

    if name == "cyclic_local":
        generators = {1, -1, 2, -2}

        graph = create_cyclic_cayley_graph(n, generators)

    elif name == "cyclic_long_jump":
        jump = n // 4
        generators = {1, -1, jump, -jump}

        graph = create_cyclic_cayley_graph(n, generators)

    elif name == "torus_2d":
        side = math.isqrt(n)

        graph = create_torus_2d_graph(side, side)

    elif name == "random_regular":
        d = 4

        graph = create_random_regular_graph(n, d, seed)

    elif name == "watts_strogatz":
        k = 4
        p = 0.1

        graph = create_watts_strogatz_graph(n, k, p, seed)

    graph.graph["family"] = name
    graph.graph["n"] = n

    if name in {"random_regular", "watts_strogatz"}:
        stochastic = True
        graph.graph["stochastic"] = stochastic

    else:
        stochastic = False
        graph.graph["stochastic"] = stochastic

    if graph.graph["stochastic"]:
        graph.graph["seed"] = seed

    else:
        graph.graph["seed"] = None
    
    graph.graph.setdefault("edge_classes", ())

    return graph
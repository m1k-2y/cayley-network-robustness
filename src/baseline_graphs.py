import networkx as nx

def create_erdos_renyi_graph(
    n: int,
    p: float,
    seed: int | None = None, 
) -> nx.Graph: 
    '''Create an Erdos-Renyi graph with the given edge probability.'''

    if n <= 0:
        raise ValueError("n must be bigger than 0.")
    
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1.")

    graph = nx.erdos_renyi_graph(n, p, seed)

    return graph

def create_barabasi_albert_graph(
    n: int,
    m: int,
    seed: int | None = None,
) -> nx.Graph:
    '''Create a Barabási–Albert graph with n nodes, attaching each new node to m existing nodes.'''
    
    if n <= 0:
        raise ValueError("n must be bigger than 0.")
    
    if m <= 0:
        raise ValueError("m must be bigger than 0.")
    
    if n <= m:
        raise ValueError("n must be bigger than m.")
    
    graph = nx.barabasi_albert_graph(n=n, m=m, seed=seed)

    return graph

def create_watts_strogatz_graph(
    n: int,
    k: int,
    p: float,
    seed: int | None = None,
) -> nx.Graph:
    '''Create a Watts–Strogatz graph with n nodes, connecting each node to k nearest neighbors and rewiring edges with probability p.'''

    if n <= 0:
        raise ValueError("n must be bigger than 0.")
    
    if not (0 < k and k < n):
        raise ValueError("k must satisfy 0 < k < n.")
    
    if k % 2 != 0:
        raise ValueError("k must be even number.")
    
    if not (0 <= p and p <= 1):
        raise ValueError("p must be between 0 to 1.")
    
    graph = nx.watts_strogatz_graph(n=n, k=k, p=p, seed=seed)

    return graph

def create_random_regular_graph(
    n: int, 
    d: int, 
    seed: int | None = None,
) -> nx.Graph:
    '''Create a random d-regular graph with n nodes.'''
    
    if n <= 0:
        raise ValueError("n must be bigger than 0.")
    
    if not 0 <= d < n:
        raise ValueError("d must be between 0 to n.") 
    
    if (n * d) % 2 != 0:
        raise ValueError("n * d must be even number.")

    graph = nx.random_regular_graph(d, n, seed)

    return graph

def create_2d_lattice_graph(
    rows: int,
    cols: int,
) -> nx.Graph:
    '''Create a 2D-Lattice graph with rows x cols.'''

    if rows <= 0:
        raise ValueError("rows must be bigger than 0.")

    if cols <= 0:
        raise ValueError("cols must be bigger than 0.")

    graph = nx.grid_2d_graph(rows, cols)

    return graph

def create_hypercube_graph(
    dimension: int,
) -> nx.Graph:
    '''Create d-dimension Hypercube graph.'''

    if dimension <= 0:
        raise ValueError("dimension must be bigger than 0.")

    graph = nx.hypercube_graph(dimension)

    return graph
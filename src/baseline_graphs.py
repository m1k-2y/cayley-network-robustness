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
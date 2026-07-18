import networkx as nx

def compute_diameter(
    graph: nx.Graph,
) -> int | None:
    
    if graph.number_of_nodes() == 0:
        return None
    
    if not nx.is_connected(graph):
        return None
    
    return nx.diameter(graph)

def compute_basic_metrics(
    graph: nx.Graph,
) -> dict:
    '''Return graph's basic metrics by computing.'''

    num_nodes = graph.number_of_nodes()

    if num_nodes == 0:
        
        info = {
            "num_nodes": 0,
            "num_edges": 0,
            "is_connected": False,
            "num_components": 0,
            "average_degree": 0.0,
            "diameter": None
        }
    
    else:
        
        info = {}

        info["num_nodes"] = num_nodes
        info["num_edges"] = graph.number_of_edges()
        info["is_connected"] = nx.is_connected(graph)
        info["num_components"] = nx.number_connected_components(graph)

        degrees = 0

        for _, degree in graph.degree():
            degrees += degree
        
        info["average_degree"] = degrees / num_nodes

        info["diameter"] = compute_diameter(graph)

    return info
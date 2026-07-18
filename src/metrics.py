import networkx as nx

def compute_diameter(
    graph: nx.Graph,
) -> int | None:
    
    if graph.number_of_nodes() == 0:
        return None
    
    if not nx.is_connected(graph):
        return None
    
    return nx.diameter(graph)

def compute_giant_component_ratio(
    graph: nx.Graph,
) -> float:
    '''Compute and return ratio of giant component.'''

    num_nodes = graph.number_of_nodes()

    if num_nodes == 0:
        return 0.0
    
    if nx.is_connected(graph):
        return 1.0
    
    largest_component_size = 0

    for component in nx.connected_components(graph):
        if len(component) > largest_component_size:
            largest_component_size = len(component)
    
    return largest_component_size / num_nodes

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
            "diameter": None,
            "giant_component_ratio": 0.0,
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
        info["giant_component_ratio"] = compute_giant_component_ratio(graph)
        
    return info
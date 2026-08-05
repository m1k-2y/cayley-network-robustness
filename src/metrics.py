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
    '''Compute the giant component ratio relative to the current graph size.'''

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

def compute_average_shortest_path_length(
    graph: nx.Graph,
) -> float | None:
    '''Compute and return average shortest path length'''
    
    num_nodes = graph.number_of_nodes()

    if num_nodes == 0:
        return None
    
    if not nx.is_connected(graph):
        return None
    
    return nx.average_shortest_path_length(graph)

def compute_basic_metrics(
    graph: nx.Graph,
) -> dict:
    '''Compute and return graph's basic metrics.'''

    num_nodes = graph.number_of_nodes()

    if num_nodes == 0:
        
        return {
            "num_nodes": 0,
            "num_edges": 0,
            "is_connected": False,
            "num_components": 0,
            "average_degree": 0.0,
            "diameter": None,
            "giant_component_ratio": 0.0,
            "average_shortest_path_length": None,
        }
    
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
    info["average_shortest_path_length"] = compute_average_shortest_path_length(graph)

    return info

def compute_component_sizes(
    graph: nx.Graph,
) -> list[int]:

    component_sizes = []

    for component in nx.connected_components(graph):
        component_sizes.append(len(component))

    component_sizes.sort(reverse=True)

    return component_sizes

def compute_component_metrics(
    graph: nx.Graph,
    initial_node_count: int,
) -> dict[str, int | float]:
    '''Compute component metrics from given graph'''

    if initial_node_count <= 0:
        raise ValueError("initial_node_count must be positive.")

    component_sizes = compute_component_sizes(graph)

    if len(component_sizes) >= 2:
        s1 = component_sizes[0] / initial_node_count
        s2 = component_sizes[1] / initial_node_count

    elif len(component_sizes) == 1:
        s1 = component_sizes[0] / initial_node_count
        s2 = 0.0

    else:
        s1 = 0.0
        s2 = 0.0

    component_metrics = {
        "remaining_nodes": graph.number_of_nodes(),
        "component_count": len(component_sizes),
        "s1": s1,
        "s2": s2,
    }

    return component_metrics
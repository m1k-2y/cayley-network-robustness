import networkx as nx

def get_largest_connected_component(
    graph: nx.Graph,
) -> nx.Graph | None:

    if graph.number_of_nodes() == 0:
        return None

    largest_component_nodes: set[int] | None = None

    for component in nx.connected_components(graph):
        if largest_component_nodes is None:
            largest_component_nodes = component

        elif len(component) > len(largest_component_nodes):
            largest_component_nodes = component

        elif len(component) == len(largest_component_nodes):
            if min(largest_component_nodes) > min(component):
                largest_component_nodes = component

    return graph.subgraph(largest_component_nodes)

def compute_diameter(
    graph: nx.Graph,
) -> int | None:
    
    largest_component = get_largest_connected_component(graph)

    if largest_component is None :
        return None

    else:
        return nx.diameter(largest_component)

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

    largest_component = get_largest_connected_component(graph)

    if largest_component is None:
        return None

    return nx.average_shortest_path_length(largest_component)

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
            "global_efficiency": 0.0,
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
    info["global_efficiency"] = compute_global_efficiency(graph)

    return info

def compute_component_sizes(
    graph: nx.Graph,
) -> list[int]:

    component_sizes = []

    for component in nx.connected_components(graph):
        component_sizes.append(len(component))

    component_sizes.sort(reverse=True)

    return component_sizes

def compute_global_efficiency(
    graph: nx.Graph,
) -> float:
    '''Compute and return graph's global efficiency'''

    if graph.number_of_nodes() == 0:
        return 0.0

    elif graph.number_of_nodes() == 1:
        return 0.0

    else:
        return nx.global_efficiency(graph)

def compute_shortest_path_metrics(
    graph: nx.Graph,
) -> tuple[int, float, float]:
    """Compute diameter_lcc, average_shortest_path_length_lcc and global_efficiency."""

    if graph.number_of_nodes() == 0:
        diameter_lcc = 0
        average_shortest_path_length_lcc = 0.0
        global_efficiency = 0.0

        return diameter_lcc, average_shortest_path_length_lcc, global_efficiency

    paths = nx.all_pairs_shortest_path_length(graph)
    lcc_nodes = set(get_largest_connected_component(graph).nodes)

    diameter_lcc = 0
    distance_sum = 0
    pair_count = 0
    efficiency_sum = 0.0

    for source, distances in paths:
        for node, distance in distances.items():
            if node in lcc_nodes:
                diameter_lcc = max(diameter_lcc, distance)

                if node != source:
                    distance_sum += distance
                    pair_count += 1

            if node != source:
                efficiency_sum += 1 / distance

    average_shortest_path_length_lcc = (
        distance_sum / pair_count if pair_count > 0 else 0.0
    )

    n = graph.number_of_nodes()
    global_efficiency = (
        efficiency_sum / (n * (n - 1)) if n > 1 else 0.0
    )

    return diameter_lcc, average_shortest_path_length_lcc, global_efficiency
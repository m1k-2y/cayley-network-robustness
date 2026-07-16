import networkx as nx
import matplotlib.pyplot as plt

def create_cyclic_cayley_graph(n, generators) :

    graph = nx.Graph()
    graph.add_nodes_from(range(n))

    for generator in generators :
        for u in range(n) :
            v = (u + generator) % n
            graph.add_edge(u, v)

    return graph

def print_graph_info(graph) :

    print("Number of nodes of the graph :", graph.number_of_nodes())
    print("Number of edges of the graph :", graph.number_of_edges())
    print("Nodes of the graph :", list(graph.nodes()))
    print("Edges of the graph :", list(graph.edges()))
    print("Degree of the graph :", dict(graph.degree()))
    print("Is the graph connected :", nx.is_connected(graph))

def draw_graph(graph, layout, filename) :

    if layout == "circular" :
        pos = nx.circular_layout(graph)

    elif layout == "spring" :
        pos = nx.spring_layout(graph)

    else :
        print("Layout must be circular or spring!")
        return

    nx.draw(graph, pos, with_labels = True)

    plt.savefig(filename)
    plt.close()

n = 5
generators = {1, -1}

cyclic = create_cyclic_cayley_graph(n, generators)

print_graph_info(cyclic)
draw_graph(cyclic, "circular", "cyclic_graph.png")

print()

n = 8
generators = {2, -2}

test_graph = create_cyclic_cayley_graph(n, generators)

print_graph_info(test_graph)
draw_graph(test_graph, "spring", "test_graph.png")
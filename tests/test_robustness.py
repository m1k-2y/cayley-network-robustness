import networkx as nx
from src.robustness import measure_attack_step

def test_measure_attack_step_connected_graph():

    graph = nx.path_graph(4)
    removed_fraction = 0.0
    initial_node_count = graph.number_of_nodes()

    step = measure_attack_step(graph, initial_node_count, removed_fraction)

    assert step['removed_fraction'] == 0.0
    assert step['remaining_nodes'] == 4
    assert step['component_count'] == 1
    assert step['giant_component_size'] == 4
    assert step['giant_component_ratio'] == 1.0
    assert step['removed_item'] is None

def test_measure_attack_step_disconnected_graph():

    graph = nx.path_graph(6)

    initial_node_count = graph.number_of_nodes()
    graph.remove_node(3)
    removed_fraction = 1 / initial_node_count
    removed_item = 3

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_item)

    assert step['removed_fraction'] == 1 / 6
    assert step['remaining_nodes'] == 5
    assert step['component_count'] == 2
    assert step['giant_component_size'] == 3
    assert step['giant_component_ratio'] == 0.5
    assert step['removed_item'] == 3

def test_measure_attack_step_empty_graph():

    graph = nx.path_graph(4)

    initial_node_count = graph.number_of_nodes()
    graph.remove_nodes_from(list(graph.nodes))
    removed_fraction = 1.0
    removed_item = 3

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_item)

    assert step['removed_fraction'] == 1.0
    assert step['remaining_nodes'] == 0
    assert step['component_count'] == 0
    assert step['giant_component_size'] == 0
    assert step['giant_component_ratio'] == 0.0
    assert step['removed_item'] == removed_item

def test_measure_attack_step_single_node_graph():

    graph = nx.path_graph(4)
    initial_node_count = graph.number_of_nodes()

    for i in range(3):
        graph.remove_node(i)

    removed_fraction = 3 / initial_node_count
    removed_item = 2

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_item)

    assert step['removed_fraction'] == removed_fraction
    assert step['remaining_nodes'] == 1
    assert step['component_count'] == 1
    assert step['giant_component_size'] == 1
    assert step['giant_component_ratio'] == 0.25
    assert step['removed_item'] == removed_item
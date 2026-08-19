import networkx as nx
import pytest
import csv
from src.results import EXPERIMENT_ROW_FIELDS
from src.robustness import measure_attack_step
from src.robustness import simulate_random_node_failure
from src.robustness import build_path_metric_checkpoints
from src.robustness import simulate_random_edge_failure
from src.results import build_experiment_row
from src.cayley_graph import create_cyclic_cayley_graph
from src.results import build_experiment_rows
from src.results import write_experiment_rows_csv
from src.robustness import simulate_hop_localized_node_failure
from src.robustness import simulate_adaptive_betweenness_node_attack
from src.robustness import simulate_generator_class_edge_failure
from src.baseline_graphs import create_random_regular_graph
from src.graph_registry import build_graph

def test_measure_attack_step_connected_graph():

    graph = nx.path_graph(4)
    removed_fraction = 0.0
    removed_count = 0
    initial_node_count = graph.number_of_nodes()

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=True)

    assert step['removed_fraction'] == 0.0
    assert step['removed_count'] == 0
    assert step['remaining_nodes'] == 4
    assert step['remaining_edges'] == 3
    assert step['component_count'] == 1
    assert step['largest_component_size'] == 4
    assert step['largest_component_ratio'] == 1.0
    assert step["second_largest_component_size"] == 0
    assert step["second_largest_component_ratio"] == 0.0
    assert step['removed_item'] is None
    assert step["diameter_lcc"] == 3
    assert step["average_shortest_path_length_lcc"] == pytest.approx(5 / 3)
    assert step["global_efficiency"] == pytest.approx(13/ 18)
    assert type(step["runtime_seconds"]) == float
    assert step["runtime_seconds"] >= 0.0

def test_measure_attack_step_disconnected_graph():

    graph = nx.path_graph(6)

    initial_node_count = graph.number_of_nodes()
    graph.remove_node(3)
    removed_fraction = 1 / initial_node_count
    removed_count = 1
    removed_item = 3

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == pytest.approx(1 / 6)
    assert step['removed_count'] == 1
    assert step['remaining_nodes'] == 5
    assert step['component_count'] == 2
    assert step['largest_component_size'] == 3
    assert step['largest_component_ratio'] == 0.5
    assert step['second_largest_component_size'] == 2
    assert step["second_largest_component_ratio"] == pytest.approx(1 / 3)
    assert step['removed_item'] == 3

def test_measure_attack_step_empty_graph():

    graph = nx.path_graph(4)

    initial_node_count = graph.number_of_nodes()
    graph.remove_nodes_from(list(graph.nodes))
    removed_fraction = 1.0
    removed_count = 4
    removed_item = 3

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == 1.0
    assert step['removed_count'] == 4
    assert step['remaining_nodes'] == 0
    assert step['component_count'] == 0
    assert step['largest_component_size'] == 0
    assert step['largest_component_ratio'] == 0.0
    assert step['second_largest_component_size'] == 0
    assert step["second_largest_component_ratio"] == 0.0
    assert step['removed_item'] == removed_item

def test_measure_attack_step_single_node_graph():

    graph = nx.path_graph(4)
    initial_node_count = graph.number_of_nodes()

    for i in range(3):
        graph.remove_node(i)

    removed_fraction = 3 / initial_node_count
    removed_count = 3
    removed_item = 2

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=True, removed_item=removed_item)

    assert step['removed_fraction'] == removed_fraction
    assert step['removed_count'] == 3
    assert step['remaining_nodes'] == 1
    assert step['component_count'] == 1
    assert step['largest_component_size'] == 1
    assert step['largest_component_ratio'] == 0.25
    assert step['second_largest_component_size'] == 0
    assert step["second_largest_component_ratio"] == 0.0
    assert step['removed_item'] == removed_item

def test_simulate_random_node_failure_basic():

    graph = nx.path_graph(4)

    history = simulate_random_node_failure(graph, seed=42)

    assert len(history) == 5
    assert history[len(history) - 1]['remaining_nodes'] == 0
    assert history[len(history) - 1]['removed_fraction'] == 1.0
    assert history[len(history) - 1]['removed_count'] == 4

    assert history[0]['remaining_nodes'] == 4
    assert history[0]['removed_fraction'] == 0.0
    assert history[0]['removed_count'] == 0
    assert history[0]['removed_item'] is None

    removed_items = []
    for step in history[1:]:
        removed_items.append(step['removed_item'])

    assert set(graph.nodes) == set(removed_items)

    assert graph.number_of_nodes() == 4

def test_build_path_metric_checkpoints_for_256_nodes():

    initial_node_count = 256

    checkpoint_count = build_path_metric_checkpoints(initial_node_count)

    assert 0 in checkpoint_count
    assert 13 in checkpoint_count
    assert 26 in checkpoint_count
    assert 256 in checkpoint_count

    assert len(checkpoint_count) == 21

def test_build_path_metric_checkpoints_rejects_nonpositive_node_count():

    initial_node_count = 0

    with pytest.raises(ValueError):
        build_path_metric_checkpoints(initial_node_count)

    initial_node_count = -1

    with pytest.raises(ValueError):
        build_path_metric_checkpoints(initial_node_count)

def test_measure_attack_step_skips_path_metrics_outside_checkpoint():

    graph = nx.path_graph(100)

    initial_node_count = graph.number_of_nodes()
    graph.remove_node(0)
    removed_fraction = 1 / initial_node_count
    removed_count = 1
    removed_item = 0

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=False, removed_item=removed_item)

    assert step["removed_fraction"] == removed_fraction
    assert step['removed_count'] == removed_count
    assert step["remaining_nodes"] == 99
    assert step["component_count"] == 1
    assert step["largest_component_size"] == 99
    assert step["largest_component_ratio"] == 0.99
    assert step["removed_item"] == removed_item
    assert step["diameter_lcc"] is None
    assert step["average_shortest_path_length_lcc"] is None
    assert step["global_efficiency"] is None
    assert type(step["runtime_seconds"]) == float
    assert step["runtime_seconds"] >= 0.0 

def test_simulate_random_node_failure_uses_path_metric_checkpoints():

    graph = nx.path_graph(100)

    history = simulate_random_node_failure(graph, seed=42)

    assert history[1]['diameter_lcc'] is None
    assert history[1]['average_shortest_path_length_lcc'] is None
    assert history[1]['global_efficiency'] is None

    assert history[5]['diameter_lcc'] is not None
    assert history[5]['average_shortest_path_length_lcc'] is not None
    assert history[5]['global_efficiency'] is not None

def test_simulate_random_edge_failure_basic():

    graph = nx.path_graph(4)

    history = simulate_random_edge_failure(graph, seed=42)

    assert len(history) == 4

    assert history[0]["removed_fraction"] == 0.0
    assert history[0]['removed_count'] == 0
    assert history[0]["removed_item"] is None

    assert history[len(history) - 1]["removed_fraction"] == 1.0
    assert history[len(history) - 1]['removed_count'] == 3
    assert history[len(history) - 1]["remaining_nodes"] == 4

    edges = set()
    for step in history[1:]:
        edges.add(step["removed_item"])

    assert set(graph.edges) == edges

def test_simulate_random_edge_failure_uses_path_metric_checkpoints():

    graph = nx.path_graph(100)

    history = simulate_random_edge_failure(graph, seed=42)

    assert history[1]["diameter_lcc"] is None
    assert history[1]["average_shortest_path_length_lcc"] is None
    assert history[1]["global_efficiency"] is None

    assert history[5]["diameter_lcc"] is not None
    assert history[5]["average_shortest_path_length_lcc"] is not None
    assert history[5]["global_efficiency"] is not None

def test_random_node_failure_is_reproducible_with_same_seed():

    graph = nx.path_graph(4)
    seed = 42

    history1 = simulate_random_node_failure(graph, seed)
    history2 = simulate_random_node_failure(graph, seed)

    for i in range(5):
        assert history1[i]["removed_item"] == history2[i]["removed_item"]

def test_random_edge_failure_is_reproducible_with_same_seed():

    graph = nx.path_graph(4)
    seed = 42

    history1 = simulate_random_edge_failure(graph, seed)
    history2 = simulate_random_edge_failure(graph, seed)

    for i in range(4):
        assert history1[i]["removed_item"] == history2[i]["removed_item"]

def test_build_experiment_row_combines_metadata_and_attack_step():

    n = 4
    generators = {1, -1}

    graph = create_cyclic_cayley_graph(n, generators)

    initial_node_count = 4

    step = measure_attack_step(graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=False)

    run_id = "test_run"
    graph_family = "cyclic_local"
    attack_type = "random"
    attack_seed = 42
    removal_type = "node"

    row = build_experiment_row(
        run_id=run_id,
        graph_family=graph_family,
        n=n, 
        graph_seed=None, 
        attack_type=attack_type, 
        attack_seed=attack_seed, 
        removal_type=removal_type,
        target_class=None,
        target_class_removal_fraction=None,
        step=step
    )

    assert row["graph_family"] == graph_family
    assert row["n"] == n
    assert row["graph_seed"] is None
    assert row["attack_type"] == attack_type
    assert row["attack_seed"] == attack_seed
    assert row["removal_type"] == removal_type

    assert row["removed_count"] == step["removed_count"]
    assert row['removed_fraction'] == step["removed_fraction"]
    assert row["largest_component_ratio"] == step["largest_component_ratio"]

    assert row["diameter_lcc"] is None
    assert row["average_shortest_path_length_lcc"] is None
    assert row["global_efficiency"] is None

    assert row["runtime_seconds"] == step["runtime_seconds"]

def test_build_experiment_rows_converts_entire_history():

    graph = nx.path_graph(4)

    history = simulate_random_node_failure(graph, seed=42)
    rows = build_experiment_rows(
        run_id="test_run",
        graph_family="path_graph",
        n=4,
        graph_seed=None,
        attack_type="random",
        attack_seed=42,
        removal_type="node",
        target_class=None,
        target_class_removal_fraction=None,
        history=history,
    )

    assert len(rows) == len(history)

    for row in rows:
        assert row["graph_family"] == "path_graph"
        assert row["n"] == 4
        assert row["graph_seed"] is None
        assert row["attack_type"] == "random"
        assert row["attack_seed"] == 42
        assert row["removal_type"] == "node"

    for i in range(len(history)):
        assert rows[i]["removed_count"] == history[i]["removed_count"]

def test_write_experiment_rows_csv_writes_header_and_rows(tmp_path):

    graph = nx.path_graph(4)

    history = simulate_random_node_failure(graph, seed=42)

    rows = build_experiment_rows(
        run_id="test_run",
        graph_family="path_graph",
        n=4,
        graph_seed=None,
        attack_type="random",
        attack_seed=42,
        removal_type="node",
        target_class=None,
        target_class_removal_fraction=None,
        history=history,
    )

    output_path = tmp_path / "results.csv"
    write_experiment_rows_csv(rows, output_path=str(output_path))

    assert output_path.exists()

    with open(output_path, encoding="utf-8", newline='') as file:
        reader = csv.DictReader(file)

        read_rows = list(reader)
        assert len(rows) == len(read_rows)

        assert reader.fieldnames == list(EXPERIMENT_ROW_FIELDS)

        assert read_rows[0]['run_id'] == "test_run"
        assert read_rows[0]['graph_family'] == "path_graph"
        assert read_rows[0]['attack_type'] == "random"
        assert read_rows[0]['attack_seed'] == "42"
        assert read_rows[0]['removed_count'] == "0"

def test_write_experiment_rows_csv_rejects_empty_rows(tmp_path):

    rows = []
    output_path = tmp_path / "results.csv"

    with pytest.raises(ValueError):
        write_experiment_rows_csv(rows, output_path)

def test_random_node_failure_respects_max_removed_fraction():

    graph = nx.path_graph(10)

    history = simulate_random_node_failure(
        graph,
        seed=42,
        max_removed_fraction=0.5,
    )

    assert history[len(history) - 1]['removed_count'] == 5
    assert history[len(history) - 1]['remaining_nodes'] == 5
    assert history[len(history) - 1]['removed_fraction'] == 0.5

    assert len(history) == 6

def test_random_node_failure_zero_max_fraction_removes_nothing():

    graph = nx.path_graph(10)

    history = simulate_random_node_failure(
        graph,
        seed=42,
        max_removed_fraction=0.0,
    )

    assert len(history) == 1

    assert history[0]["removed_count"] == 0
    assert history[0]["removed_fraction"] == 0.0
    assert history[0]["remaining_nodes"] == 10
    assert history[0]["removed_item"] is None

def test_random_node_failure_rejects_invalid_max_removed_fraction():

    graph = nx.path_graph(10)

    with pytest.raises(ValueError):
        simulate_random_node_failure(graph, seed=42, max_removed_fraction=-0.1)

    with pytest.raises(ValueError):
        simulate_random_node_failure(graph, seed=42, max_removed_fraction=1.1)

def test_random_edge_failure_respects_max_removed_fraction():

    graph = nx.path_graph(11)

    history = simulate_random_edge_failure(graph, seed=42, max_removed_fraction=0.5)

    assert history[len(history) - 1]["removed_count"] == 5
    assert history[len(history) - 1]["remaining_edges"] == 5
    assert history[len(history) - 1]["removed_fraction"] == 0.5

    assert len(history) == 6

def test_random_edge_failure_zero_max_fraction_removes_nothing():

    graph = nx.path_graph(11)

    history = simulate_random_edge_failure(graph, seed=42, max_removed_fraction=0.0)
    assert len(history) == 1

    assert history[0]["removed_count"] == 0
    assert history[0]["remaining_edges"] == 10
    assert history[0]["removed_fraction"] == 0.0
    assert history[0]["removed_item"] is None

def test_random_edge_failure_rejects_invalid_max_removed_fraction():

    graph = nx.path_graph(11)

    with pytest.raises(ValueError):
        simulate_random_edge_failure(graph, seed=42, max_removed_fraction=-0.1)

    with pytest.raises(ValueError):
        simulate_random_edge_failure(graph, seed=42, max_removed_fraction=1.1)

def test_measure_attack_step_computes_algebraic_connectivity_at_checkpoint():

    graph = nx.path_graph(3)
    initial_node_count = graph.number_of_nodes()

    step = measure_attack_step(graph, initial_node_count, removed_fraction=0.0, removed_count=0, is_path_metric_checkpoint=True)

    assert step["algebraic_connectivity"] == pytest.approx(1.0)

def test_measure_attack_step_skips_algebraic_connectivity_outside_checkpoint():

    graph = nx.path_graph(3)
    initial_node_count = graph.number_of_nodes()

    graph.remove_node(0)
    removed_fraction = 1 / initial_node_count
    removed_count = 1

    step = measure_attack_step(graph, initial_node_count, removed_fraction, removed_count, is_path_metric_checkpoint=False)

    assert step["algebraic_connectivity"] is None

def test_build_experiment_row_preserves_algebraic_connectivity():

    graph = nx.path_graph(3)
    initial_node_count = graph.number_of_nodes()

    step = measure_attack_step(
        graph,
        initial_node_count,
        removed_fraction=0.0,
        removed_count=0,
        is_path_metric_checkpoint=True,
    )

    row = build_experiment_row(
        run_id="test_run",
        graph_family="path_graph",
        n=3,
        graph_seed=None,
        attack_type="random",
        attack_seed=42,
        removal_type="node",
        target_class=None,
        target_class_removal_fraction=None,
        step=step,
    )

    assert row["algebraic_connectivity"] == step["algebraic_connectivity"]

def test_hop_localized_node_failure_removes_all_nodes():

    graph = nx.path_graph(5)

    history = simulate_hop_localized_node_failure(graph, seed=42)

    assert len(history) == 6
    assert history[5]['removed_count'] == 5
    assert history[5]["remaining_nodes"] == 0
    assert history[5]['removed_fraction'] == 1.0

def test_hop_localized_node_failure_respects_max_removed_fraction():

    graph = nx.path_graph(10)

    history = simulate_hop_localized_node_failure(graph, seed=42, max_removed_fraction=0.5)

    assert len(history) == 6
    assert history[5]['removed_count'] == 5
    assert history[5]['remaining_nodes'] == 5
    assert history[5]['removed_fraction'] == 0.5

def test_hop_localized_node_failure_zero_max_fraction_removes_nothing():

    graph = nx.path_graph(10)

    history = simulate_hop_localized_node_failure(graph, seed=42, max_removed_fraction=0.0)

    assert len(history) == 1
    assert history[0]['removed_count'] == 0
    assert history[0]['remaining_nodes'] == 10
    assert history[0]['removed_fraction'] == 0.0
    assert history[0]['removed_item'] is None

def test_hop_localized_node_failure_rejects_invalid_max_removed_fraction():

    graph = nx.path_graph(10)

    with pytest.raises(ValueError):
        simulate_hop_localized_node_failure(graph, seed=42, max_removed_fraction=-0.1)

    with pytest.raises(ValueError):
        simulate_hop_localized_node_failure(graph, seed=42, max_removed_fraction=1.1)

def test_hop_localized_node_failure_rejects_disconnected_graph():

    graph = nx.path_graph(2)
    graph.add_node(2)

    with pytest.raises(ValueError):
        simulate_hop_localized_node_failure(graph, seed=42)

def test_hop_localized_node_failure_empty_graph_returns_empty_history():

    graph = nx.Graph()

    history = simulate_hop_localized_node_failure(graph, seed=42)

    assert history == []

def test_hop_localized_node_failure_is_reproducible_with_same_seed():

    n = 10
    generators = {-1, 1}

    graph = create_cyclic_cayley_graph(n, generators)

    history1 = simulate_hop_localized_node_failure(graph, seed=42)
    history2 = simulate_hop_localized_node_failure(graph, seed=42)

    for i in range(1, len(history1)):
        assert history1[i]['removed_item'] == history2[i]['removed_item']

def test_hop_localized_node_failure_removes_nodes_in_nondecreasing_hop_distance():

    n = 10
    generators = {-1, 1}

    graph = create_cyclic_cayley_graph(n, generators)

    history = simulate_hop_localized_node_failure(graph, seed=42)

    start_node = history[1]['removed_item']

    path_length = nx.single_source_shortest_path_length(graph, start_node)

    for i in range(1, len(history) - 1):
        length1 = path_length[history[i]['removed_item']]
        length2 = path_length[history[i + 1]['removed_item']]

        assert length1 <= length2

def test_adaptive_betweenness_attack_removes_highest_betweenness_node_first():

    graph = nx.path_graph(5)

    history = simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=0.2)

    assert len(history) == 2
    assert history[1]["removed_item"] == 2
    assert history[1]["removed_count"] == 1
    assert history[1]["remaining_nodes"] == 4

def test_adaptive_betweenness_attack_recomputes_centrality_after_each_removal():

    graph = nx.Graph()

    graph.add_edges_from([
        (0, 4),
        (0, 5),
        (3, 4),
        (1, 3),
        (2, 3)
    ])

    history = simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=1 / 3)

    assert history[1]["removed_item"] == 3
    assert history[2]["removed_item"] == 0

def test_adaptive_betweenness_attack_is_reproducible_with_same_seed():

    graph1 = create_cyclic_cayley_graph(n=6, generators={-1, 1})
    graph2 = create_cyclic_cayley_graph(n=6, generators={-1, 1})

    history1 = simulate_adaptive_betweenness_node_attack(graph1, seed=42, max_removed_fraction=1 / 6)
    history2 = simulate_adaptive_betweenness_node_attack(graph2, seed=42, max_removed_fraction=1 / 6)

    assert history1[1]["removed_item"] == history2[1]["removed_item"]

def test_adaptive_betweenness_attack_respects_max_removed_fraction():

    graph = nx.path_graph(10)

    history = simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=0.5)

    assert len(history) == 6
    assert history[5]["remaining_nodes"] == 5
    assert history[5]["removed_count"] == 5
    assert history[5]["removed_fraction"] == 0.5

def test_adaptive_betweenness_attack_zero_max_fraction_removes_nothing():

    graph = nx.path_graph(10)

    history = simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=0.0)

    assert len(history) == 1
    assert history[0]["remaining_nodes"] == 10
    assert history[0]["removed_count"] == 0
    assert history[0]["removed_fraction"] == 0.0

def test_adaptive_betweenness_attack_rejects_invalid_max_removed_fraction():

    graph = nx.path_graph(10)

    with pytest.raises(ValueError):
        simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=-0.1)

    with pytest.raises(ValueError):
        simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=1.1)

def test_adaptive_betweenness_attack_rejects_invalid_k():

    graph = nx.path_graph(10)

    with pytest.raises(ValueError):
        simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=0.0, k=0)

    with pytest.raises(ValueError):
        simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=0.0, k=-1)

def test_adaptive_betweenness_attack_with_k_is_reproducible():

    graph1 = nx.path_graph(10)
    graph2 = nx.path_graph(10)

    history1 = simulate_adaptive_betweenness_node_attack(graph1, seed=42, max_removed_fraction=1 / 5, k=3)
    history2 = simulate_adaptive_betweenness_node_attack(graph2, seed=42, max_removed_fraction=1 / 5, k=3)

    for i in range(1, len(history1)):
        assert history1[i]["removed_item"] == history2[i]["removed_item"]

def test_adaptive_betweenness_attack_caps_k_at_remaining_node_count():

    graph = nx.path_graph(5)

    history = simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=1.0, k=64)

    assert len(history) == 6
    assert history[5]["remaining_nodes"] == 0
    assert history[5]["removed_count"] == 5
    assert history[5]["removed_fraction"] == 1.0

def test_adaptive_betweenness_attack_empty_graph_returns_empty_history():

    graph = nx.Graph()

    history = simulate_adaptive_betweenness_node_attack(graph, seed=42, max_removed_fraction=1.0)

    assert history == []

def test_generator_class_edge_failure_removes_target_class_edges():

    n = 10
    generators = {-1, 1, -2, 2}

    graph = create_cyclic_cayley_graph(n, generators)   

    history = simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=1.0)

    assert history[10]["removed_count"] == 10
    assert history[10]["remaining_edges"] == 10

def test_generator_class_edge_failure_removes_only_target_class():

    n = 10
    generators = {-1, 1, -2, 2}

    graph = create_cyclic_cayley_graph(n, generators)

    history = simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=1.0)

    removed_edges = []

    for i in range(1, len(history)):
        removed_edges.append(tuple(sorted((history[i]["removed_item"]))))

    step_1_edges = []

    for (u, v, data) in graph.edges(data=True):
        if data["edge_class"] == "step_1":
            step_1_edges.append(tuple(sorted((u, v))))

    assert set(step_1_edges) == set(removed_edges)

def test_generator_class_edge_failure_respects_target_class_removal_fraction():

    n = 10
    generators = {-1, 1, -2, 2}

    graph = create_cyclic_cayley_graph(n, generators)

    history = simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=0.5)

    assert history[-1]["removed_count"] == 5

def test_generator_class_edge_failure_zero_fraction_returns_initial_step_only():

    n = 10
    generators = {-1, 1, -2, 2}

    graph = create_cyclic_cayley_graph(n, generators)

    history = simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=0.0)

    assert len(history) == 1
    assert history[0]["removed_count"] == 0
    assert history[0]["removed_fraction"] == 0.0
    assert history[0]["remaining_edges"] == 20

def test_generator_class_edge_failure_rejects_invalid_fraction():

    n = 10
    generators = {-1, 1, -2, 2}
    
    graph = create_cyclic_cayley_graph(n, generators)

    with pytest.raises(ValueError):
        simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=-0.1)

    with pytest.raises(ValueError):
        simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=1.1)

def test_generator_class_edge_failure_rejects_invalid_target_class():

    n = 10
    generators = {-1, 1, -2, 2}
        
    graph = create_cyclic_cayley_graph(n, generators)

    with pytest.raises(ValueError):
        simulate_generator_class_edge_failure(graph, seed=42, target_class="horizontal", target_class_removal_fraction=0.5)

def test_generator_class_edge_failure_is_reproducible_with_same_seed():

    n = 10
    generators = {-1, 1, -2, 2}
            
    graph = create_cyclic_cayley_graph(n, generators)

    history1 = simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=0.5)
    history2 = simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=0.5)

    for i in range(1, len(history1)):
        assert tuple(sorted(history1[i]["removed_item"])) == tuple(sorted(history2[i]["removed_item"]))

def test_generator_class_edge_failure_rejects_graph_without_edge_classes():

    graph = build_graph("random_regular", n=256, seed=42)

    with pytest.raises(ValueError):
        simulate_generator_class_edge_failure(graph, seed=42, target_class="step_1", target_class_removal_fraction=0.5)

def test_initial_normalized_global_efficiency_equals_global_efficiency_initially():

    graph = nx.path_graph(4)

    step = measure_attack_step(
        graph,
        initial_node_count=4,
        removed_fraction=0.0,
        removed_count=0,
        is_path_metric_checkpoint=True,
    )

    assert step["initial_normalized_global_efficiency"] == pytest.approx(
        step["global_efficiency"]
    )

def test_initial_normalized_global_efficiency_uses_initial_node_count():

    graph = nx.path_graph(4)
    graph.remove_node(3)

    step = measure_attack_step(
        graph,
        initial_node_count=4,
        removed_fraction=0.25,
        removed_count=1,
        is_path_metric_checkpoint=True,
    )

    expected = (
        step["global_efficiency"]
        * 3
        * 2
        / (4 * 3)
    )

    assert step["initial_normalized_global_efficiency"] == pytest.approx(expected)

def test_initial_normalized_global_efficiency_equals_global_efficiency_for_edge_removal():

    graph = nx.cycle_graph(4)
    graph.remove_edge(0, 1)

    step = measure_attack_step(
        graph,
        initial_node_count=4,
        removed_fraction=0.25,
        removed_count=1,
        is_path_metric_checkpoint=True,
    )

    assert step["initial_normalized_global_efficiency"] == pytest.approx(
        step["global_efficiency"]
    )

def test_initial_normalized_global_efficiency_is_none_outside_checkpoint():

    graph = nx.path_graph(4)

    step = measure_attack_step(
        graph,
        initial_node_count=4,
        removed_fraction=0.25,
        removed_count=1,
        is_path_metric_checkpoint=False,
    )

    assert step["global_efficiency"] is None
    assert step["initial_normalized_global_efficiency"] is None

def test_experiment_row_fields_include_initial_normalized_global_efficiency():

    assert "initial_normalized_global_efficiency" in EXPERIMENT_ROW_FIELDS

def test_build_experiment_row_copies_initial_normalized_global_efficiency():

    step = {
        "removed_fraction": 0.0,
        "removed_count": 0,
        "remaining_nodes": 4,
        "remaining_edges": 3,
        "component_count": 1,
        "largest_component_size": 4,
        "largest_component_ratio": 1.0,
        "second_largest_component_size": 0,
        "second_largest_component_ratio": 0.0,
        "removed_item": None,
        "diameter_lcc": 3,
        "average_shortest_path_length_lcc": 1.6666666666666667,
        "global_efficiency": 0.7222222222222222,
        "initial_normalized_global_efficiency": 0.7222222222222222,
        "runtime_seconds": 0.01,
        "algebraic_connectivity": 0.585786437626905,
    }

    row = build_experiment_row(
        run_id="test",
        graph_family="test_graph",
        n=4,
        graph_seed=None,
        attack_type="random_node",
        attack_seed=42,
        removal_type="node",
        target_class=None,
        target_class_removal_fraction=None,
        step=step,
    )

    assert row["initial_normalized_global_efficiency"] == (
        step["initial_normalized_global_efficiency"]
    )
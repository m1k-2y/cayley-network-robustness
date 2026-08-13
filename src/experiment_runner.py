from src.graph_registry import build_graph
from src.robustness import simulate_hop_localized_node_failure
from src.robustness import simulate_random_edge_failure
from src.robustness import simulate_random_node_failure
from src.results import build_experiment_rows
from src.results import ExperimentRow

def run_single_experiment(
    run_id: str,
    graph_family: str,
    n: int,
    graph_seed: int | None,
    attack_type: str,
    attack_seed: int | None,
    max_removed_fraction: float = 1.0,

) -> list[ExperimentRow]:

    graph = build_graph(graph_family, n, seed=graph_seed)

    if attack_type == "random_node":
        history = simulate_random_node_failure(graph, seed=attack_seed, max_removed_fraction=max_removed_fraction)
        removal_type = "node"
        target_class = None
        target_class_removal_fraction = None

    elif attack_type == "random_edge":
        history = simulate_random_edge_failure(graph, seed=attack_seed, max_removed_fraction=max_removed_fraction)
        removal_type = "edge"
        target_class = None
        target_class_removal_fraction = None

    elif attack_type == "hop_localized":
        history = simulate_hop_localized_node_failure(graph, seed=attack_seed, max_removed_fraction=max_removed_fraction)
        removal_type = "node"
        target_class = None
        target_class_removal_fraction = None

    else:
        raise ValueError("unsupported attack_type")
    
    rows = build_experiment_rows(
        run_id=run_id,
        graph_family=graph_family,
        n=n,
        graph_seed=graph_seed,
        attack_type=attack_type,
        attack_seed=attack_seed,
        removal_type=removal_type,
        target_class=target_class,
        target_class_removal_fraction=target_class_removal_fraction,
        history=history,
    )

    return rows
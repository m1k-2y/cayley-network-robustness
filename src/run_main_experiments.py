from src.batch_runner import run_batch_experiments
from src.results import write_experiment_rows_csv
from pathlib import Path

def run_experiment_slice(
    graph_family: str,
    n: int,
    attack_type: str,
    attack_seeds: list[int],
    graph_seeds: list[int],
):

    if attack_type == "generator_class" and (graph_family == "watts_strogatz" or graph_family == "random_regular"):
        return

    run_id_prefix = "main"

    if attack_type in ("random_node", "random_edge", "generator_class", "hop_localized"):
        max_removed_fraction = 1.0

    elif attack_type == "adaptive_betweenness":
        max_removed_fraction = 0.5

    else:
        raise ValueError("Invalid attack_type.")

    rows = run_batch_experiments(
        run_id_prefix=run_id_prefix,
        graph_families=[graph_family],
        node_counts=[n],
        attack_types=[attack_type],
        attack_seeds=attack_seeds,
        graph_seeds=graph_seeds,
        generator_class_removal_fraction=1.0,
        max_removed_fraction=max_removed_fraction,
        adaptive_k=None,
    )

    Path("results").mkdir(exist_ok=True)

    output_path = "results/n" + str(n) + "_" + graph_family + "_" + attack_type + ".csv"

    write_experiment_rows_csv(
        rows=rows,
        output_path=output_path,
    )
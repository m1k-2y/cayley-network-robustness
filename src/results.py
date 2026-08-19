import csv
from typing import TypedDict
from src.robustness import AttackStep
from src.robustness import AttackHistory

class ExperimentRow(TypedDict):
    run_id: str
    graph_family: str
    n: int
    graph_seed: int | None
    attack_type: str
    attack_seed: int | None
    removal_type: str
    target_class: str | None
    target_class_removal_fraction: float | None
    removed_fraction: float
    removed_count: int
    remaining_nodes: int
    remaining_edges: int
    component_count: int
    largest_component_size: int
    largest_component_ratio: float
    second_largest_component_size: int
    second_largest_component_ratio: float
    diameter_lcc: int | None
    average_shortest_path_length_lcc: float | None
    global_efficiency: float | None
    initial_normalized_global_efficiency: float | None
    algebraic_connectivity: float | None
    runtime_seconds: float | None

EXPERIMENT_ROW_FIELDS = (
    "run_id",
    "graph_family",
    "n",
    "graph_seed",
    "attack_type",
    "attack_seed",
    "removal_type",
    "target_class",
    "target_class_removal_fraction",
    "removed_fraction",
    "removed_count",
    "remaining_nodes",
    "remaining_edges",
    "component_count",
    "largest_component_size",
    "largest_component_ratio",
    "second_largest_component_size",
    "second_largest_component_ratio",
    "diameter_lcc",
    "average_shortest_path_length_lcc",
    "global_efficiency",
    "initial_normalized_global_efficiency",
    "algebraic_connectivity",
    "runtime_seconds",
)
 
def build_experiment_row(
    run_id: str,
    graph_family: str,
    n: int,
    graph_seed: int | None,
    attack_type: str,
    attack_seed: int | None,
    removal_type: str,
    target_class: str | None,
    target_class_removal_fraction: float | None,
    step: AttackStep,
) -> ExperimentRow:
    '''Build experiment row.'''

    row : ExperimentRow = {
        "run_id": run_id,
        "graph_family": graph_family,
        "n": n,
        "graph_seed": graph_seed,
        "attack_type": attack_type,
        "attack_seed": attack_seed,
        "removal_type": removal_type,
        "target_class": target_class,
        "target_class_removal_fraction": target_class_removal_fraction,
        "removed_fraction": step["removed_fraction"],
        "removed_count": step["removed_count"],
        "remaining_nodes": step["remaining_nodes"],
        "remaining_edges": step["remaining_edges"],
        "component_count": step["component_count"],
        "largest_component_size": step["largest_component_size"],
        "largest_component_ratio": step["largest_component_ratio"],
        "second_largest_component_size": step["second_largest_component_size"],
        "second_largest_component_ratio": step["second_largest_component_ratio"],
        "diameter_lcc": step["diameter_lcc"],
        "average_shortest_path_length_lcc": step["average_shortest_path_length_lcc"],
        "global_efficiency": step["global_efficiency"],
        "initial_normalized_global_efficiency": step["initial_normalized_global_efficiency"],
        "algebraic_connectivity": step["algebraic_connectivity"],
        "runtime_seconds": step["runtime_seconds"],
    }

    return row

def build_experiment_rows(
    run_id: str,
    graph_family: str,
    n: int,
    graph_seed: int | None,
    attack_type: str,
    attack_seed: int | None,
    removal_type: str,
    target_class: str | None,
    target_class_removal_fraction: float | None,
    history: AttackHistory,
) -> list[ExperimentRow]:
    '''Build experiment rows list.'''

    rows : list[ExperimentRow] = []

    for step in history:
        row = build_experiment_row(run_id, graph_family, n, graph_seed, attack_type, attack_seed, removal_type, target_class, target_class_removal_fraction, step)
        rows.append(row)

    return rows

def write_experiment_rows_csv(
    rows: list[ExperimentRow],
    output_path: str,
) -> None:
    '''Save csv file.'''

    if len(rows) == 0:
        raise ValueError("row must not be empty.")

    with open(output_path, 'w', encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=EXPERIMENT_ROW_FIELDS)

        writer.writeheader()
        for row in rows:
            writer.writerow(row)
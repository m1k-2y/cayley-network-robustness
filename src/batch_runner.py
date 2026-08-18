from src.experiment_runner import run_single_experiment
from src.results import ExperimentRow

GENERATOR_CLASS_TARGETS: dict[tuple[str, int], list[str]] = {
    ("cyclic_local", 256): ["step_1", "step_2"],
    ("cyclic_local", 1024): ["step_1", "step_2"],

    ("cyclic_long_jump", 256): ["step_1", "step_64"],
    ("cyclic_long_jump", 1024): ["step_1", "step_256"],

    ("torus_2d", 256): ["horizontal", "vertical"],
    ("torus_2d", 1024): ["horizontal", "vertical"],
}

def run_batch_experiments(
    run_id_prefix: str,
    graph_families: list[str],
    node_counts: list[int],
    attack_types: list[str],
    attack_seeds: list[int],
    graph_seeds: list[int],
    generator_class_removal_fraction: float = 1.0,
    max_removed_fraction: float = 1.0,
    adaptive_k: int | None = None,
) -> list[ExperimentRow]:

    all_rows = []

    for node_count in node_counts:
        for graph_family in graph_families:
            if graph_family in ("cyclic_local", "cyclic_long_jump", "torus_2d"):
                graph_seed = None
                for attack_seed in attack_seeds:
                    for attack_type in attack_types:
                        if attack_type in ("random_node", "random_edge", "hop_localized", "adaptive_betweenness"):
                            run_id = run_id_prefix + "_" + graph_family + "_n" + str(node_count) + "_" + attack_type + "_gnone_a" + str(attack_seed)
                            rows = run_single_experiment(
                                run_id=run_id,
                                graph_family=graph_family,
                                n=node_count,
                                graph_seed=graph_seed,
                                attack_type=attack_type,
                                attack_seed=attack_seed,
                                max_removed_fraction=max_removed_fraction,
                                k=adaptive_k,
                                target_class=None,
                                target_class_removal_fraction=generator_class_removal_fraction,
                            )

                            all_rows.extend(rows)

                        elif attack_type == "generator_class":
                            for target_class in GENERATOR_CLASS_TARGETS[(graph_family, node_count)]:
                                run_id = run_id_prefix + "_" + graph_family + "_n" + str(node_count) + "_generator_class_" + target_class + "_gnone_a" + str(attack_seed)
                                rows = run_single_experiment(
                                    run_id=run_id,
                                    graph_family=graph_family,
                                    n=node_count,
                                    graph_seed=graph_seed,
                                    attack_type=attack_type,
                                    attack_seed=attack_seed,
                                    max_removed_fraction=max_removed_fraction,
                                    k=adaptive_k,
                                    target_class=target_class,
                                    target_class_removal_fraction=generator_class_removal_fraction
                                )

                                all_rows.extend(rows)

                        else:
                            raise ValueError("unsupported attack_type.")

            elif graph_family in ("random_regular", "watts_strogatz"):
                for graph_seed in graph_seeds:
                    for attack_seed in attack_seeds:
                        for attack_type in attack_types:
                            if attack_type in ("random_node", "random_edge", "hop_localized", "adaptive_betweenness"):
                                run_id = run_id_prefix + "_" + graph_family + "_n" + str(node_count) + "_" + attack_type + "_g" + str(graph_seed) + "_a" + str(attack_seed)
                                rows = run_single_experiment(
                                    run_id=run_id,
                                    graph_family=graph_family,
                                    n=node_count,
                                    graph_seed=graph_seed,
                                    attack_type=attack_type,
                                    attack_seed=attack_seed,
                                    max_removed_fraction=max_removed_fraction,
                                    k=adaptive_k,
                                    target_class=None,
                                    target_class_removal_fraction=generator_class_removal_fraction,
                                )

                                all_rows.extend(rows)

                            elif attack_type == "generator_class":
                                continue

                            else:
                                raise ValueError("unsupported attack_type.")
            else:
                raise ValueError("unsupported graph_family.")
            
    return all_rows
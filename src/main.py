from src.run_main_experiments import run_experiment_slice

def main():

    graph_families = [
        "cyclic_local",
        "cyclic_long_jump",
        "torus_2d",
        "random_regular",
        "watts_strogatz",
    ]

    node_counts = [
        256,
        1024,
    ]

    attack_types = [
        "random_node",
        "random_edge",
        "hop_localized",
        "adaptive_betweenness",
        "generator_class",
    ]

    attack_seeds = [42]

    graph_seeds = [42]

    for graph_family in graph_families:
        for n in node_counts:
            for attack_type in attack_types:
                run_experiment_slice(graph_family, n, attack_type, attack_seeds, graph_seeds)

if __name__ == "__main__":
    main()

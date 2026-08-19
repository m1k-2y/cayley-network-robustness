from src.batch_runner import run_batch_experiments

all_rows = run_batch_experiments(
    run_id_prefix="smoke",
    graph_families=["cyclic_local", "cyclic_long_jump", "torus_2d", "random_regular", "watts_strogatz"] ,
    node_counts=[256],
    attack_types=["random_node", "random_edge", "hop_localized", "adaptive_betweenness", "generator_class"],
    attack_seeds=[42],
    graph_seeds=[42],
    max_removed_fraction=0.01,
    generator_class_removal_fraction=0.01,
    adaptive_k=8,
)

print(len(all_rows))

run_id_set = set()
for row in all_rows:
    run_id_set.add(row["run_id"])
print(len(run_id_set))
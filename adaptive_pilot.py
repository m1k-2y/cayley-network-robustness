import time

from src.batch_runner import run_batch_experiments


start = time.perf_counter()

rows = run_batch_experiments(
    run_id_prefix="random_regular_exact_n1024",
    graph_families=["random_regular"],
    node_counts=[1024],
    attack_types=["adaptive_betweenness"],
    attack_seeds=[42],
    graph_seeds=[42],
    max_removed_fraction=0.01,
    adaptive_k=None,
)

elapsed = time.perf_counter() - start

print("rows:", len(rows))
print("runtime:", elapsed)

if len(rows) > 1:
    print("removed_count:", rows[-1]["removed_count"])
    print(
        "runtime per removal step:",
        elapsed / (len(rows) - 1),
    )
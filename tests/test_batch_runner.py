from src.batch_runner import run_batch_experiments
import pytest

def test_run_batch_experiments_deterministic_graph():

    all_rows = run_batch_experiments(
        run_id_prefix="batch",
        graph_families=["cyclic_local"],
        node_counts=[256],
        attack_types=["random_node"],
        attack_seeds=[42, 43],
        graph_seeds=[1, 2], 
        max_removed_fraction=0.01,
    )

    assert len(all_rows) == 6
    for row in all_rows:
        assert row["graph_seed"] is None
        assert row["attack_seed"] in (42, 43)
        assert row["run_id"] in ("batch_cyclic_local_n256_random_node_gnone_a42", "batch_cyclic_local_n256_random_node_gnone_a43")

def test_run_batch_experiments_stochastic_graph():

    all_rows = run_batch_experiments(
        run_id_prefix="batch",
        graph_families=["random_regular"],
        node_counts=[256],
        attack_types=["random_node"],
        attack_seeds=[42],
        graph_seeds=[1, 2],
        max_removed_fraction=0.01,
    )

    assert len(all_rows) == 6
    for row in all_rows:
        assert row["graph_seed"] in (1, 2)
        assert row["attack_seed"] == 42
        assert row["run_id"] in ("batch_random_regular_n256_random_node_g1_a42", "batch_random_regular_n256_random_node_g2_a42")

def test_run_batch_experiments_generator_class():

    all_rows = run_batch_experiments(
        run_id_prefix="batch",
        graph_families=["cyclic_local"],
        node_counts=[256],
        attack_types=["generator_class"],
        attack_seeds=[42],
        graph_seeds=[1, 2],   
        generator_class_removal_fraction=0.01,
    )

    assert len(all_rows) == 6
    for row in all_rows:
        assert row["graph_seed"] is None
        assert row["attack_seed"] == 42
        assert row["target_class"] in ("step_1", "step_2")
        assert row["target_class_removal_fraction"] == 0.01
        assert row["run_id"] in ("batch_cyclic_local_n256_generator_class_step_1_gnone_a42", "batch_cyclic_local_n256_generator_class_step_2_gnone_a42")

def test_run_batch_experiments_rejects_unsupported_attack_type():

    with pytest.raises(ValueError):
        run_batch_experiments(
            run_id_prefix="batch",
            graph_families=["cyclic_local"],
            node_counts=[256],
            attack_types=["unknown"],
            attack_seeds=[42],
            graph_seeds=[1],
        )

def test_run_batch_experiments_rejects_unsupported_graph_family():

    with pytest.raises(ValueError):
        run_batch_experiments(
            run_id_prefix="batch",
            graph_families=["unknown"],
            node_counts=[256],
            attack_types=["random_node"],
            attack_seeds=[42],
            graph_seeds=[1],
        )

def test_run_batch_experiments_skips_generator_class_for_non_structural_graph():

    all_rows = run_batch_experiments(
        run_id_prefix="batch",
        graph_families=["random_regular"],
        node_counts=[256],
        attack_types=["generator_class"],
        attack_seeds=[42],
        graph_seeds=[1, 2],
    )

    assert all_rows == [] 

def test_run_batch_experiments_mixed_batch():

    all_rows = run_batch_experiments(
        run_id_prefix="batch",
        graph_families=["cyclic_local", "random_regular"],
        node_counts=[256],
        attack_types=["random_node", "generator_class"],
        attack_seeds=[42],
        graph_seeds=[1],
        max_removed_fraction=0.01,
        generator_class_removal_fraction=0.01,
    )

    assert len(all_rows) == 12
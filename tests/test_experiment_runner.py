from src.experiment_runner import run_single_experiment
import pytest

def test_run_single_experiment_random_node():

    rows = run_single_experiment(
        run_id="test_run",
        graph_family="cyclic_local",
        n=256,
        graph_seed=None,
        attack_type="random_node",
        attack_seed=42,
        max_removed_fraction=0.01,
    )

    assert len(rows) == 3
    assert rows[-1]["removed_count"] == 2
    assert rows[-1]["remaining_nodes"] == 254

    assert rows[0]["run_id"] == "test_run"
    assert rows[0]["graph_family"] == "cyclic_local"
    assert rows[0]["n"] == 256
    assert rows[0]["graph_seed"] is None
    assert rows[0]["attack_type"] == "random_node"
    assert rows[0]["attack_seed"] == 42
    assert rows[0]["removal_type"] == "node"
    assert rows[0]["target_class"] is None
    assert rows[0]["target_class_removal_fraction"] is None

def test_run_single_experiment_random_edge():

    rows = run_single_experiment(
        run_id="test_run",
        graph_family="cyclic_local",
        n=256,
        graph_seed=None,
        attack_type="random_edge",
        attack_seed=42,
        max_removed_fraction=0.01,
    )

    assert len(rows) == 6
    assert rows[-1]["removed_count"] == 5
    assert rows[-1]["remaining_edges"] == 507

    assert rows[0]["run_id"] == "test_run"
    assert rows[0]["graph_family"] == "cyclic_local"
    assert rows[0]["n"] == 256
    assert rows[0]["graph_seed"] is None
    assert rows[0]["attack_type"] == "random_edge"
    assert rows[0]["attack_seed"] == 42
    assert rows[0]["removal_type"] == "edge"
    assert rows[0]["target_class"] is None
    assert rows[0]["target_class_removal_fraction"] is None

def test_run_single_experiment_hop_localized():

    rows = run_single_experiment(
        run_id="test_run",
        graph_family="cyclic_local",
        n=256,
        graph_seed=None,
        attack_type="hop_localized",
        attack_seed=42,
        max_removed_fraction=0.01,
    )

    assert len(rows) == 3
    assert rows[-1]["removed_count"] == 2
    assert rows[-1]["remaining_nodes"] == 254

    assert rows[0]["run_id"] == "test_run"
    assert rows[0]["graph_family"] == "cyclic_local"
    assert rows[0]["n"] == 256
    assert rows[0]["graph_seed"] is None
    assert rows[0]["attack_type"] == "hop_localized"
    assert rows[0]["attack_seed"] == 42
    assert rows[0]["removal_type"] == "node"
    assert rows[0]["target_class"] is None
    assert rows[0]["target_class_removal_fraction"] is None

def test_run_single_experiment_rejects_unsupported_attack_type():

    with pytest.raises(ValueError):
        run_single_experiment(
            run_id="test_run",
            graph_family="cyclic_local",
            n=256,
            graph_seed=None,
            attack_type="unknown",
            attack_seed=42,
            max_removed_fraction=0.01,
        )

def test_run_single_experiment_records_actual_graph_seed():

    rows = run_single_experiment(
        run_id="test_run",
        graph_family="cyclic_local",
        n=256,
        graph_seed=42,
        attack_type="random_node",
        attack_seed=42,
        max_removed_fraction=0.01,
    )

    assert rows[0]["graph_seed"] is None

def test_run_single_experiment_requires_attack_seed():

    with pytest.raises(ValueError):
        run_single_experiment(
            run_id="test_run",
            graph_family="cyclic_local",
            n=256,
            graph_seed=None,
            attack_type="random_node",
            attack_seed=None,
            max_removed_fraction=0.01,
        )
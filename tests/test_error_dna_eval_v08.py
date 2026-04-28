import json

import pytest

import evals.run_error_dna_eval as dna_runner


@pytest.fixture(scope="session")
def report():
    return dna_runner.run_error_dna_eval()


def test_report_is_dict(report):
    assert isinstance(report, dict)


def test_total_histories_at_least_five(report):
    assert report["total_histories"] >= 5


def test_all_histories_pass(report):
    assert report["passed_histories"] == report["total_histories"]


def test_pass_rate_is_one(report):
    assert report["pass_rate"] == 1.0


def test_every_history_has_top_weaknesses(report):
    for history in report["histories"]:
        assert "top_weaknesses" in history
        assert isinstance(history["top_weaknesses"], list)


def test_every_history_has_teacher_review_needed_count(report):
    for history in report["histories"]:
        assert "teacher_review_needed_count" in history
        assert isinstance(history["teacher_review_needed_count"], int)


def test_report_is_json_serializable(report):
    encoded = json.dumps(report)
    decoded = json.loads(encoded)
    assert decoded["total_histories"] == report["total_histories"]


def test_save_json_report_writes_valid_json(tmp_path):
    r = dna_runner.run_error_dna_eval()
    output_path = tmp_path / "eval_reports" / "error_dna_eval.json"

    dna_runner.save_json_report(r, str(output_path))

    assert output_path.exists()
    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded["total_histories"] == r["total_histories"]
    assert loaded["pass_rate"] == 1.0

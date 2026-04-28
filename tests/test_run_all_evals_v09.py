import json
from pathlib import Path
from unittest.mock import patch

import pytest

from evals.run_all_evals import run_all_evals, save_json_report


@pytest.fixture(scope="module")
def all_evals_report():
    return run_all_evals()


def test_report_is_dict(all_evals_report):
    assert isinstance(all_evals_report, dict)


def test_report_contains_synthetic_eval(all_evals_report):
    assert "synthetic_eval" in all_evals_report


def test_report_contains_error_dna_eval(all_evals_report):
    assert "error_dna_eval" in all_evals_report


def test_overall_passed_is_true(all_evals_report):
    assert all_evals_report["overall_passed"] is True


def test_total_failures_is_zero(all_evals_report):
    assert all_evals_report["total_failures"] == 0


def test_report_is_json_serializable(all_evals_report):
    serialized = json.dumps(all_evals_report)
    assert isinstance(serialized, str)


def test_save_json_report_writes_file(tmp_path: Path, all_evals_report):
    output_file = tmp_path / "subdir" / "all_evals.json"
    save_json_report(all_evals_report, str(output_file))
    assert output_file.exists()
    loaded = json.loads(output_file.read_text(encoding="utf-8"))
    assert loaded["overall_passed"] is True


def test_fail_on_regression_exits_zero_when_all_pass():
    with patch("sys.argv", ["run_all_evals", "--fail-on-regression"]):
        with pytest.raises(SystemExit) as exc_info:
            from evals.run_all_evals import main
            main()
        assert exc_info.value.code == 0


def test_overall_passed_false_when_synthetic_fails():
    failing_synthetic = {"failed_cases": 1}
    passing_dna = {"failed_histories": 0}
    with patch("evals.run_all_evals.run_synthetic_eval", return_value=failing_synthetic), \
         patch("evals.run_all_evals.run_error_dna_eval", return_value=passing_dna):
        report = run_all_evals()
    assert report["overall_passed"] is False
    assert report["total_failures"] == 1


def test_overall_passed_false_when_dna_fails():
    passing_synthetic = {"failed_cases": 0}
    failing_dna = {"failed_histories": 2}
    with patch("evals.run_all_evals.run_synthetic_eval", return_value=passing_synthetic), \
         patch("evals.run_all_evals.run_error_dna_eval", return_value=failing_dna):
        report = run_all_evals()
    assert report["overall_passed"] is False
    assert report["total_failures"] == 2


def test_total_failures_sums_both_evals():
    failing_synthetic = {"failed_cases": 3}
    failing_dna = {"failed_histories": 2}
    with patch("evals.run_all_evals.run_synthetic_eval", return_value=failing_synthetic), \
         patch("evals.run_all_evals.run_error_dna_eval", return_value=failing_dna):
        report = run_all_evals()
    assert report["total_failures"] == 5


def test_fail_on_regression_exits_one_when_evals_fail():
    failing_synthetic = {
        "failed_cases": 1,
        "passed_cases": 24,
        "total_cases": 25,
        "pass_rate": 0.96,
        "average_awarded_marks": 7.0,
        "teacher_review_rate": 0.4,
    }
    failing_dna = {
        "failed_histories": 0,
        "passed_histories": 5,
        "total_histories": 5,
        "pass_rate": 1.0,
    }
    with patch("evals.run_all_evals.run_synthetic_eval", return_value=failing_synthetic), \
         patch("evals.run_all_evals.run_error_dna_eval", return_value=failing_dna), \
         patch("sys.argv", ["run_all_evals", "--fail-on-regression"]):
        with pytest.raises(SystemExit) as exc_info:
            from evals.run_all_evals import main
            main()
        assert exc_info.value.code == 1

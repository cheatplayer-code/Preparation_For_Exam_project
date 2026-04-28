import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from evals.run_all_evals import run_all_evals, save_json_report


def test_report_is_dict():
    report = run_all_evals()
    assert isinstance(report, dict)


def test_report_contains_synthetic_eval():
    report = run_all_evals()
    assert "synthetic_eval" in report


def test_report_contains_error_dna_eval():
    report = run_all_evals()
    assert "error_dna_eval" in report


def test_overall_passed_is_true():
    report = run_all_evals()
    assert report["overall_passed"] is True


def test_total_failures_is_zero():
    report = run_all_evals()
    assert report["total_failures"] == 0


def test_report_is_json_serializable():
    report = run_all_evals()
    serialized = json.dumps(report)
    assert isinstance(serialized, str)


def test_save_json_report_writes_file(tmp_path: Path):
    report = run_all_evals()
    output_file = tmp_path / "subdir" / "all_evals.json"
    save_json_report(report, str(output_file))
    assert output_file.exists()
    loaded = json.loads(output_file.read_text(encoding="utf-8"))
    assert loaded["overall_passed"] is True


def test_fail_on_regression_exits_zero_when_all_pass():
    with patch("sys.argv", ["run_all_evals", "--fail-on-regression"]):
        with pytest.raises(SystemExit) as exc_info:
            from evals.run_all_evals import main
            main()
        assert exc_info.value.code == 0

import json

import evals.run_synthetic_eval as eval_runner


def test_v06_failure_category_counts_has_expected_keys():
    report = eval_runner.run_synthetic_eval()
    assert set(report["failure_category_counts"].keys()) == {
        "marks_regression",
        "error_taxonomy_regression",
        "confidence_regression",
        "review_flag_regression",
    }


def test_v06_failure_category_counts_zero_when_all_cases_pass(monkeypatch):
    cases = [
        {
            "case_id": "case_pass",
            "solution_text": "final answer: x=1",
            "expected_answer": "x=1",
            "confirmed_by_student": True,
            "input_source": "typed",
            "expected_awarded_marks": 10,
            "expected_error_types": [],
            "expected_confidence": "high",
            "expected_teacher_review_needed": False,
        }
    ]

    def fake_mark_solution(_payload, expected_answer=None):
        return {
            "awarded_marks": 10,
            "error_types": [],
            "confidence": "high",
            "teacher_review_needed": False,
        }

    monkeypatch.setattr(eval_runner, "SYNTHETIC_SOLUTIONS", cases)
    monkeypatch.setattr(eval_runner, "mark_solution", fake_mark_solution)

    report = eval_runner.run_synthetic_eval()
    assert report["failed_cases"] == 0
    assert report["failure_category_counts"] == {
        "marks_regression": 0,
        "error_taxonomy_regression": 0,
        "confidence_regression": 0,
        "review_flag_regression": 0,
    }


def test_v06_build_markdown_report_shape_and_content():
    report = eval_runner.run_synthetic_eval()
    markdown = eval_runner.build_markdown_report(report)

    assert isinstance(markdown, str)
    assert "Synthetic Evaluation Report" in markdown
    assert f"total cases: {report['total_cases']}" in markdown
    assert f"pass rate: {report['pass_rate']:.1%}" in markdown


def test_v06_save_json_report_writes_valid_json_file(tmp_path):
    report = eval_runner.run_synthetic_eval()
    output_path = tmp_path / "eval_reports" / "synthetic_eval.json"

    eval_runner.save_json_report(report, str(output_path))

    assert output_path.exists()
    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded["total_cases"] == report["total_cases"]


def test_v06_save_markdown_report_writes_file(tmp_path):
    report = eval_runner.run_synthetic_eval()
    output_path = tmp_path / "eval_reports" / "synthetic_eval.md"

    eval_runner.save_markdown_report(report, str(output_path))

    assert output_path.exists()
    markdown = output_path.read_text(encoding="utf-8")
    assert "Synthetic Evaluation Report" in markdown


def test_v06_run_synthetic_eval_is_json_serializable():
    report = eval_runner.run_synthetic_eval()
    encoded = json.dumps(report)
    decoded = json.loads(encoded)
    assert decoded["total_cases"] == report["total_cases"]

import json

from evals.run_synthetic_eval import run_synthetic_eval


def test_run_synthetic_eval_returns_report_dict():
    report = run_synthetic_eval()
    assert isinstance(report, dict)


def test_v05_report_summary_metrics_stable():
    report = run_synthetic_eval()

    assert report["total_cases"] == 25
    assert report["passed_cases"] == 25
    assert report["pass_rate"] == 1.0


def test_v05_report_confidence_distribution_keys():
    report = run_synthetic_eval()
    assert set(report["confidence_distribution"].keys()) == {"high", "medium", "low"}


def test_v05_teacher_review_rate_is_calculated_correctly():
    report = run_synthetic_eval()
    case_results = report["case_results"]
    expected_rate = sum(1 for case in case_results if case["actual"]["teacher_review_needed"]) / len(case_results)
    assert report["teacher_review_rate"] == expected_rate


def test_v05_report_is_json_serializable():
    report = run_synthetic_eval()
    encoded = json.dumps(report)
    decoded = json.loads(encoded)
    assert decoded["total_cases"] == report["total_cases"]


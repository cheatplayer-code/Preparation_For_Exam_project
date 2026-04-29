import json

from demo.run_student_demo import (
    build_demo_summary,
    run_student_demo,
    save_json_report,
)


def test_run_student_demo_returns_report_dict():
    report = run_student_demo()
    assert isinstance(report, dict)


def test_run_student_demo_report_shape():
    report = run_student_demo()
    assert report["student_id"] == "demo_student_001"
    assert len(report["attempts"]) == 4
    assert report["summary"]["attempt_count"] == 4
    assert isinstance(report["summary"]["average_percentage"], float)
    assert isinstance(report["summary"]["teacher_review_needed_count"], int)
    assert report["error_dna_profile"] is not None
    assert report["study_plan"] is not None
    assert len(report["study_plan"]["days"]) == 7


def test_run_student_demo_report_json_serializable():
    report = run_student_demo()
    encoded = json.dumps(report)
    decoded = json.loads(encoded)
    assert decoded["student_id"] == report["student_id"]


def test_save_json_report_writes_valid_json(tmp_path):
    report = run_student_demo()
    output_path = tmp_path / "demo_reports" / "student_demo.json"
    save_json_report(report, str(output_path))
    assert output_path.exists()
    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded["student_id"] == report["student_id"]


def test_build_demo_summary_contains_student_id():
    report = run_student_demo()
    summary = build_demo_summary(report)
    assert isinstance(summary, str)
    assert "demo_student_001" in summary

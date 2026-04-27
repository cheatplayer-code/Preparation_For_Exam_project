import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from evals.synthetic_v04_cases import SYNTHETIC_SOLUTIONS
from model_core.rubric_engine import mark_solution


def _solution_payload(case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "solution_text": case["solution_text"],
        "student_id": case["case_id"],
        "question_id": case["case_id"],
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": case["confirmed_by_student"],
        "input_source": case["input_source"],
    }


def _expected_outcome(case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "awarded_marks": case["expected_awarded_marks"],
        "error_types": sorted(case["expected_error_types"]),
        "confidence": case["expected_confidence"],
        "teacher_review_needed": case["expected_teacher_review_needed"],
    }


def _actual_outcome(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "awarded_marks": result["awarded_marks"],
        "error_types": sorted(result["error_types"]),
        "confidence": result["confidence"],
        "teacher_review_needed": result["teacher_review_needed"],
    }


def _collect_mismatches(expected: Dict[str, Any], actual: Dict[str, Any]) -> List[Dict[str, Any]]:
    mismatches = []
    for key in ("awarded_marks", "error_types", "confidence", "teacher_review_needed"):
        if expected[key] != actual[key]:
            mismatches.append(
                {
                    "field": key,
                    "expected": expected[key],
                    "actual": actual[key],
                }
            )
    return mismatches


def extract_failure_categories_from_mismatches(mismatches: List[Dict[str, Any]]) -> List[str]:
    category_by_field = {
        "awarded_marks": "marks_regression",
        "error_types": "error_taxonomy_regression",
        "confidence": "confidence_regression",
        "teacher_review_needed": "review_flag_regression",
    }
    categories = []
    for mismatch in mismatches:
        category = category_by_field.get(mismatch["field"])
        if category and category not in categories:
            categories.append(category)
    return categories


def build_markdown_report(report: Dict[str, Any]) -> str:
    lines = [
        "# Synthetic Evaluation Report",
        "",
        f"- total cases: {report['total_cases']}",
        f"- passed cases: {report['passed_cases']}",
        f"- failed cases: {report['failed_cases']}",
        f"- pass rate: {report['pass_rate']:.1%}",
        f"- average awarded marks: {report['average_awarded_marks']:.2f}",
        f"- teacher review rate: {report['teacher_review_rate']:.1%}",
        "- confidence distribution:",
        f"  - high: {report['confidence_distribution']['high']}",
        f"  - medium: {report['confidence_distribution']['medium']}",
        f"  - low: {report['confidence_distribution']['low']}",
        "",
    ]

    failures = report.get("failures", [])
    if failures:
        lines.extend(
            [
                "## Failures",
                "",
                "| case_id | categories | mismatch_fields |",
                "| --- | --- | --- |",
            ]
        )
        for failure in failures:
            categories = ", ".join(failure.get("failure_categories", []))
            mismatch_fields = ", ".join(mismatch["field"] for mismatch in failure.get("mismatches", []))
            lines.append(f"| {failure['case_id']} | {categories} | {mismatch_fields} |")
        lines.append("")

    lines.append("This eval checks deterministic stability, not real exam validity.")
    return "\n".join(lines)


def save_json_report(report: Dict[str, Any], path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def save_markdown_report(report: Dict[str, Any], path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_markdown_report(report) + "\n", encoding="utf-8")


def build_summary_line(report: Dict[str, Any]) -> str:
    return (
        "Synthetic evaluation: "
        f"{report['passed_cases']}/{report['total_cases']} passed "
        f"({report['pass_rate']:.1%}), avg_marks={report['average_awarded_marks']:.2f}, "
        f"teacher_review_rate={report['teacher_review_rate']:.1%}"
    )


def run_synthetic_eval() -> Dict[str, Any]:
    case_results = []
    failures = []
    confidence_distribution = {"high": 0, "medium": 0, "low": 0}
    failure_category_counts = {
        "marks_regression": 0,
        "error_taxonomy_regression": 0,
        "confidence_regression": 0,
        "review_flag_regression": 0,
    }
    total_awarded_marks = 0
    teacher_review_count = 0

    for case in SYNTHETIC_SOLUTIONS:
        result = mark_solution(_solution_payload(case), expected_answer=case["expected_answer"])
        expected = _expected_outcome(case)
        actual = _actual_outcome(result)
        mismatches = _collect_mismatches(expected, actual)
        passed = len(mismatches) == 0

        case_result = {
            "case_id": case["case_id"],
            "passed": passed,
            "expected": expected,
            "actual": actual,
            "mismatches": mismatches,
        }
        case_results.append(case_result)

        if not passed:
            case_result["failure_categories"] = extract_failure_categories_from_mismatches(mismatches)
            for category in case_result["failure_categories"]:
                failure_category_counts[category] += 1
            failures.append(case_result)

        total_awarded_marks += float(actual["awarded_marks"])
        if actual["teacher_review_needed"]:
            teacher_review_count += 1
        if actual["confidence"] in confidence_distribution:
            confidence_distribution[actual["confidence"]] += 1

    total_cases = len(SYNTHETIC_SOLUTIONS)
    passed_cases = len(case_results) - len(failures)
    failed_cases = len(failures)

    report = {
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "pass_rate": passed_cases / total_cases if total_cases else 0.0,
        "average_awarded_marks": total_awarded_marks / total_cases if total_cases else 0.0,
        "teacher_review_rate": teacher_review_count / total_cases if total_cases else 0.0,
        "confidence_distribution": confidence_distribution,
        "failure_category_counts": failure_category_counts,
        "failures": failures,
        "case_results": case_results,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run synthetic stability evaluation for model-core.")
    parser.add_argument("--json-only", action="store_true", help="Print only the JSON report.")
    parser.add_argument("--summary-only", action="store_true", help="Print only the summary line.")
    parser.add_argument("--output", type=str, help="Write the full JSON report to the provided path.")
    parser.add_argument("--markdown-output", type=str, help="Write a markdown summary report to the provided path.")
    parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit with status code 1 when any synthetic case fails.",
    )
    args = parser.parse_args()

    report = run_synthetic_eval()
    summary = build_summary_line(report)

    if args.output:
        save_json_report(report, args.output)
    if args.markdown_output:
        save_markdown_report(report, args.markdown_output)

    if args.summary_only:
        print(summary)
    elif args.json_only:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(summary)
        print(json.dumps(report, indent=2, sort_keys=True))

    if args.fail_on_regression:
        raise SystemExit(1 if report["failed_cases"] > 0 else 0)


if __name__ == "__main__":
    main()

import argparse
import json
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


def run_synthetic_eval() -> Dict[str, Any]:
    case_results = []
    failures = []
    confidence_distribution = {"high": 0, "medium": 0, "low": 0}
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
        "failures": failures,
        "case_results": case_results,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run synthetic stability evaluation for model-core.")
    parser.add_argument("--json-only", action="store_true", help="Print only the JSON report.")
    args = parser.parse_args()

    report = run_synthetic_eval()

    if not args.json_only:
        print(
            "Synthetic evaluation: "
            f"{report['passed_cases']}/{report['total_cases']} passed "
            f"({report['pass_rate']:.1%}), avg_marks={report['average_awarded_marks']:.2f}, "
            f"teacher_review_rate={report['teacher_review_rate']:.1%}"
        )

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

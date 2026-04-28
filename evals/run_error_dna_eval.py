import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from evals.student_histories_v08 import STUDENT_HISTORIES
from evals.synthetic_v04_cases import SYNTHETIC_SOLUTIONS
from model_core.error_dna import update_error_dna
from model_core.rubric_engine import mark_solution
from model_core.study_plan import generate_7_day_plan


def _solution_payload(case: Dict[str, Any], student_id: str) -> Dict[str, Any]:
    return {
        "solution_text": case["solution_text"],
        "student_id": student_id,
        "question_id": case["case_id"],
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": case["confirmed_by_student"],
        "input_source": case["input_source"],
    }


def _collect_mismatches(
    teacher_review_count: int,
    top_weaknesses: List[str],
    plan_focus_categories: List[str],
    history: Dict[str, Any],
) -> List[Dict[str, Any]]:
    mismatches: List[Dict[str, Any]] = []

    expected_count = history["expected_teacher_review_needed_count"]
    if teacher_review_count != expected_count:
        mismatches.append(
            {
                "field": "teacher_review_needed_count",
                "expected": expected_count,
                "actual": teacher_review_count,
            }
        )

    for weakness in history["expected_top_weaknesses"]:
        if weakness not in top_weaknesses:
            mismatches.append(
                {
                    "field": "top_weaknesses",
                    "expected_contains": weakness,
                    "actual": top_weaknesses,
                }
            )

    for category in history["expected_plan_focus_contains"]:
        if category not in plan_focus_categories:
            mismatches.append(
                {
                    "field": "plan_focus_categories",
                    "expected_contains": category,
                    "actual": plan_focus_categories,
                }
            )

    return mismatches


def run_error_dna_eval() -> Dict[str, Any]:
    solutions_by_id = {case["case_id"]: case for case in SYNTHETIC_SOLUTIONS}

    history_results: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    for history in STUDENT_HISTORIES:
        student_id = history["student_id"]

        profile: Optional[Dict[str, Any]] = None
        teacher_review_count = 0

        for case_id in history["attempts"]:
            case = solutions_by_id[case_id]
            result = mark_solution(
                _solution_payload(case, student_id),
                expected_answer=case["expected_answer"],
            )
            profile = update_error_dna(student_id, result, current_profile=profile)
            if result["teacher_review_needed"]:
                teacher_review_count += 1

        plan = generate_7_day_plan(profile)
        plan_focus_categories = sorted(
            {day["focus_error_category"] for day in plan["days"]}
        )

        weaknesses: Dict[str, float] = (profile or {}).get("weaknesses", {})
        top_weaknesses = [
            cat
            for cat, score in sorted(weaknesses.items(), key=lambda kv: kv[1], reverse=True)
            if score > 0
        ]

        mismatches = _collect_mismatches(
            teacher_review_count, top_weaknesses, plan_focus_categories, history
        )
        passed = len(mismatches) == 0

        history_result: Dict[str, Any] = {
            "student_id": student_id,
            "passed": passed,
            "description": history["description"],
            "attempt_count": len(history["attempts"]),
            "teacher_review_needed_count": teacher_review_count,
            "top_weaknesses": top_weaknesses,
            "expected_top_weaknesses": history["expected_top_weaknesses"],
            "plan_focus_categories": plan_focus_categories,
            "expected_plan_focus_contains": history["expected_plan_focus_contains"],
            "mismatches": mismatches,
        }
        history_results.append(history_result)

        if not passed:
            failures.append(history_result)

    total_histories = len(STUDENT_HISTORIES)
    passed_histories = total_histories - len(failures)

    return {
        "total_histories": total_histories,
        "passed_histories": passed_histories,
        "failed_histories": len(failures),
        "pass_rate": passed_histories / total_histories if total_histories else 0.0,
        "histories": history_results,
        "failures": failures,
    }


def build_summary_line(report: Dict[str, Any]) -> str:
    return (
        "Error DNA evaluation: "
        f"{report['passed_histories']}/{report['total_histories']} passed "
        f"({report['pass_rate']:.1%})"
    )


def save_json_report(report: Dict[str, Any], path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Error DNA aggregation evaluation for model-core v0.8."
    )
    parser.add_argument("--json-only", action="store_true", help="Print only the JSON report.")
    parser.add_argument("--summary-only", action="store_true", help="Print only the summary line.")
    parser.add_argument("--output", type=str, help="Write the full JSON report to the provided path.")
    parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit with status code 1 when any student history fails.",
    )
    args = parser.parse_args()

    report = run_error_dna_eval()
    summary = build_summary_line(report)

    if args.output:
        save_json_report(report, args.output)

    if args.summary_only:
        print(summary)
    elif args.json_only:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(summary)
        print(json.dumps(report, indent=2, sort_keys=True))

    if args.fail_on_regression:
        raise SystemExit(1 if report["failed_histories"] > 0 else 0)


if __name__ == "__main__":
    main()

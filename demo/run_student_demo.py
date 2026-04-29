import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from evals.synthetic_v04_cases import SYNTHETIC_SOLUTIONS
from model_core.error_dna import update_error_dna
from model_core.rubric_engine import mark_solution
from model_core.study_plan import generate_7_day_plan

DEMO_STUDENT_ID = "demo_student_001"
DEMO_CASE_IDS = [
    "synthetic_02_missing_reasoning",
    "synthetic_03_wrong_final_answer",
    "synthetic_04_concept_gap",
    "synthetic_25_manual_edit_clean_confirmed",
]


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


def _collect_top_error_types(error_counts: Dict[str, int]) -> List[str]:
    return [
        err
        for err, _ in sorted(error_counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def run_student_demo() -> Dict[str, Any]:
    solutions_by_id = {case["case_id"]: case for case in SYNTHETIC_SOLUTIONS}
    attempts: List[Dict[str, Any]] = []
    profile: Optional[Dict[str, Any]] = None
    error_counts: Dict[str, int] = {}
    teacher_review_needed_count = 0

    for case_id in DEMO_CASE_IDS:
        case = solutions_by_id[case_id]
        solution_input = _solution_payload(case, DEMO_STUDENT_ID)
        marking = mark_solution(solution_input, expected_answer=case["expected_answer"])
        profile = update_error_dna(DEMO_STUDENT_ID, marking, current_profile=profile)

        if marking["teacher_review_needed"]:
            teacher_review_needed_count += 1
        for err in marking.get("error_types", []):
            error_counts[err] = error_counts.get(err, 0) + 1

        attempts.append(
            {
                "case_id": case_id,
                "awarded_marks": marking["awarded_marks"],
                "total_marks": marking["total_marks"],
                "percentage": marking["percentage"],
                "error_types": marking["error_types"],
                "confidence": marking["confidence"],
                "teacher_review_needed": marking["teacher_review_needed"],
                "feedback_summary": marking["feedback_summary"],
                "rewrite_guidance": marking["rewrite_guidance"],
            }
        )

    study_plan = generate_7_day_plan(profile or {})
    average_percentage = (
        sum(attempt["percentage"] for attempt in attempts) / len(attempts)
        if attempts
        else 0.0
    )

    report = {
        "student_id": DEMO_STUDENT_ID,
        "attempts": attempts,
        "error_dna_profile": profile,
        "study_plan": study_plan,
        "summary": {
            "attempt_count": len(attempts),
            "average_percentage": float(average_percentage),
            "teacher_review_needed_count": int(teacher_review_needed_count),
            "top_error_types": _collect_top_error_types(error_counts),
        },
    }
    return report


def build_demo_summary(report: Dict[str, Any]) -> str:
    summary = report.get("summary", {})
    lines = [
        f"Student demo report for {report.get('student_id')}",
        f"Attempts: {summary.get('attempt_count')} | "
        f"Avg score: {summary.get('average_percentage', 0.0):.2f}% | "
        f"Teacher reviews: {summary.get('teacher_review_needed_count')}",
    ]
    top_errors = summary.get("top_error_types", [])
    if top_errors:
        lines.append(f"Top error types: {', '.join(top_errors)}")
    else:
        lines.append("Top error types: none")

    lines.append("Attempt highlights:")
    for attempt in report.get("attempts", []):
        lines.append(
            f"- {attempt['case_id']}: {attempt['awarded_marks']}/"
            f"{attempt['total_marks']} ({attempt['percentage']:.2f}%), "
            f"errors={', '.join(attempt['error_types']) or 'none'}"
        )

    plan_days = report.get("study_plan", {}).get("days", [])
    lines.append(f"Study plan days: {len(plan_days)}")
    return "\n".join(lines)


def save_json_report(report: Dict[str, Any], path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the v1.1 student demo flow.")
    parser.add_argument("--json-only", action="store_true", help="Print only the JSON report.")
    parser.add_argument("--summary-only", action="store_true", help="Print only the summary.")
    parser.add_argument("--output", type=str, help="Write the full JSON report to the provided path.")
    args = parser.parse_args()

    report = run_student_demo()
    summary = build_demo_summary(report)

    if args.output:
        save_json_report(report, args.output)

    if args.summary_only:
        print(summary)
    elif args.json_only:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(summary)
        print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

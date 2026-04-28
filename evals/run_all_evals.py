import argparse
import json
from pathlib import Path
from typing import Any, Dict

from evals.run_synthetic_eval import run_synthetic_eval
from evals.run_error_dna_eval import run_error_dna_eval


def run_all_evals() -> Dict[str, Any]:
    synthetic = run_synthetic_eval()
    error_dna = run_error_dna_eval()

    total_failures = synthetic["failed_cases"] + error_dna["failed_histories"]
    overall_passed = synthetic["failed_cases"] == 0 and error_dna["failed_histories"] == 0

    return {
        "synthetic_eval": synthetic,
        "error_dna_eval": error_dna,
        "overall_passed": overall_passed,
        "total_failures": total_failures,
    }


def build_summary_lines(report: Dict[str, Any]) -> str:
    s = report["synthetic_eval"]
    e = report["error_dna_eval"]
    lines = [
        f"Synthetic eval:  {s['passed_cases']}/{s['total_cases']} passed ({s['pass_rate']:.1%})",
        f"Error DNA eval:  {e['passed_histories']}/{e['total_histories']} passed ({e['pass_rate']:.1%})",
        f"Overall passed:  {report['overall_passed']}",
        f"Total failures:  {report['total_failures']}",
    ]
    return "\n".join(lines)


def save_json_report(report: Dict[str, Any], path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run all evaluations (synthetic + Error DNA) for model-core v0.9."
    )
    parser.add_argument("--json-only", action="store_true", help="Print only the JSON report.")
    parser.add_argument("--summary-only", action="store_true", help="Print only the summary lines.")
    parser.add_argument("--output", type=str, help="Write the full JSON report to the provided path.")
    parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit with status code 1 when any eval fails.",
    )
    args = parser.parse_args()

    report = run_all_evals()
    summary = build_summary_lines(report)

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
        raise SystemExit(0 if report["overall_passed"] else 1)


if __name__ == "__main__":
    main()

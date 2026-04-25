import re
from typing import Dict, Iterable, List, Union

from .confidence import assess_confidence
from .models import CriterionResult, MarkingResult, StudentSolutionInput


def _normalize(s: str) -> str:
    return re.sub(r"\s+", "", (s or "").strip().lower())


def _extract_final_answer(text: str) -> str:
    patterns = [
        r"final\s+answer\s*[:=]\s*([^\n]+)",
        r"answer\s*[:=]\s*([^\n]+)",
        r"therefore\s*,?\s*([^\n]+)",
        r"thus\s*,?\s*([^\n]+)",
    ]
    lowered = text.lower()
    for p in patterns:
        m = re.search(p, lowered)
        if m:
            return m.group(1).strip().strip(".")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-1].lower().strip(".") if lines else ""


def _has_any(text: str, tokens: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in tokens)


def mark_solution(
    solution_input: Union[StudentSolutionInput, Dict[str, object]],
    expected_answer: str | None = None,
) -> Dict[str, object]:
    if isinstance(solution_input, dict):
        solution_input = StudentSolutionInput(**solution_input)

    text = solution_input.solution_text.strip()
    lowered = text.lower()

    has_reasoning = _has_any(lowered, ["because", "therefore", "since", "hence", "step", "then"])
    has_method = _has_any(
        lowered,
        ["equation", "substitute", "simplify", "factor", "integrate", "differentiate", "isolate", "solve"],
    )
    unclear = _has_any(lowered, ["???", "idk", "not sure", "unclear", "..."])
    conceptual_misunderstanding = _has_any(
        lowered,
        [
            "triangle has four sides",
            "derivative of x is x",
            "denominator + denominator",
            "multiply fractions by adding",
        ],
    )

    criterion_results: List[CriterionResult] = []

    correctness = 4
    correctness_errors: List[str] = []
    correctness_feedback = "Final answer aligns with expected outcome."

    extracted_final = _extract_final_answer(text)
    if not extracted_final:
        correctness = 2
        correctness_errors.append("incomplete_final_answer")
        correctness_feedback = "Final answer is missing or not clearly stated."
    elif expected_answer is not None and _normalize(extracted_final) != _normalize(expected_answer):
        correctness = 1
        correctness_errors.append("incomplete_final_answer")
        correctness_feedback = "Final answer is not correct even though work may contain useful steps."

    if conceptual_misunderstanding:
        correctness = min(correctness, 1)
        correctness_errors.append("concept_gap")
        correctness_feedback = "The response shows conceptual misunderstanding of core ideas."

    criterion_results.append(
        CriterionResult(
            criterion="correctness",
            max_score=4,
            awarded_score=correctness,
            lost_marks=4 - correctness,
            error_types=sorted(set(correctness_errors)),
            feedback=correctness_feedback,
        )
    )

    method = 3 if has_method else 1
    method_errors = [] if has_method else ["method_gap"]
    method_feedback = "Method steps are present and follow a valid process." if has_method else "Method is incomplete or not visible."
    if conceptual_misunderstanding:
        method = min(method, 1)
        method_errors = sorted(set(method_errors + ["concept_gap"]))
        method_feedback = "Method reflects a concept-level misunderstanding."

    criterion_results.append(
        CriterionResult(
            criterion="method",
            max_score=3,
            awarded_score=method,
            lost_marks=3 - method,
            error_types=method_errors,
            feedback=method_feedback,
        )
    )

    reasoning = 2 if has_reasoning else 0
    reasoning_errors = [] if has_reasoning else ["missing_reasoning"]
    criterion_results.append(
        CriterionResult(
            criterion="reasoning",
            max_score=2,
            awarded_score=reasoning,
            lost_marks=2 - reasoning,
            error_types=reasoning_errors,
            feedback="Reasoning is explicit and understandable." if has_reasoning else "Reasoning is missing.",
        )
    )

    clarity = 1
    clarity_errors: List[str] = []
    clarity_feedback = "Working is clear."
    if unclear or len(text) < 20:
        clarity = 0
        clarity_errors.append("unclear_working")
        clarity_feedback = "Working is unclear or too brief to verify."

    criterion_results.append(
        CriterionResult(
            criterion="clarity",
            max_score=1,
            awarded_score=clarity,
            lost_marks=1 - clarity,
            error_types=clarity_errors,
            feedback=clarity_feedback,
        )
    )

    total_score = sum(c.awarded_score for c in criterion_results)
    max_score = sum(c.max_score for c in criterion_results)
    lost_marks = max_score - total_score

    all_errors = sorted({e for c in criterion_results for e in c.error_types})
    evidence_strength = total_score / max_score if max_score else 0.0
    confidence_result = assess_confidence(
        solution_text=text,
        confirmed_by_student=solution_input.confirmed_by_student,
        evidence_strength=evidence_strength,
        error_types=all_errors,
    )

    feedback_summary = (
        f"Scored {total_score}/{max_score}. "
        + ("Key issues: " + ", ".join(all_errors) if all_errors else "No major issues detected.")
    )
    rewrite_guidance = (
        "State the final answer clearly, show method steps, and explain why each step is valid."
        if all_errors
        else "Keep the same structure and clarity in future responses."
    )

    result = MarkingResult(
        student_id=solution_input.student_id,
        question_id=solution_input.question_id,
        topic=solution_input.topic,
        subskill=solution_input.subskill,
        criterion_results=criterion_results,
        total_score=total_score,
        max_score=max_score,
        lost_marks=lost_marks,
        error_types=all_errors,
        feedback_summary=feedback_summary,
        rewrite_guidance=rewrite_guidance,
        confidence=confidence_result["confidence"],
        teacher_review_needed=bool(confidence_result["teacher_review_needed"]),
    )
    return result.to_dict()

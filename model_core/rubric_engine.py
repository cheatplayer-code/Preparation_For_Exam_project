import re
from typing import Dict, Iterable, List, Optional, Union

from .confidence import assess_confidence
from .models import (
    ALLOWED_INPUT_SOURCES,
    ERROR_DNA_CATEGORIES,
    CriterionResult,
    MarkingResult,
    MIN_SOLUTION_LENGTH,
    StudentSolutionInput,
)
from .symbolic_validator import validate_final_answer


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
    # Intentional fallback: use the last non-empty line as probable final answer
    # when explicit markers like "final answer:" are absent.
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-1].lower().strip(".") if lines else ""


def _has_any(text: str, tokens: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in tokens)


def _validate_solution_input(solution_input: StudentSolutionInput) -> None:
    if not isinstance(solution_input.confirmed_by_student, bool):
        raise ValueError("confirmed_by_student must be a boolean.")

    if solution_input.input_source not in ALLOWED_INPUT_SOURCES:
        raise ValueError(f"input_source must be one of: {', '.join(ALLOWED_INPUT_SOURCES)}.")

    if not isinstance(solution_input.solution_text, str) or not solution_input.solution_text.strip():
        raise ValueError("solution_text must be non-empty.")

    if not isinstance(solution_input.topic, str) or not solution_input.topic.strip():
        raise ValueError("topic must be non-empty.")

    if not isinstance(solution_input.subskill, str) or not solution_input.subskill.strip():
        raise ValueError("subskill must be non-empty.")


def mark_solution(
    solution_input: Union[StudentSolutionInput, Dict[str, object]],
    expected_answer: Optional[str] = None,
) -> Dict[str, object]:
    if isinstance(solution_input, dict):
        try:
            solution_input = StudentSolutionInput(**solution_input)
        except TypeError as exc:
            raise ValueError(f"Invalid solution input payload: {exc}") from exc

    _validate_solution_input(solution_input)

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
    symbolic_validation = None

    correctness = 4
    correctness_errors: List[str] = []
    correctness_feedback = "Final answer aligns with expected outcome."
    correctness_evidence_found: List[str] = []
    correctness_evidence_missing: List[str] = []
    correctness_decision_reason = "Final answer was identified and matched expected answer."
    correctness_verifiable = False

    extracted_final = _extract_final_answer(text)
    if not extracted_final:
        correctness = 2
        correctness_errors.append("incomplete_final_answer")
        correctness_feedback = "Final answer is missing or not clearly stated."
        correctness_evidence_missing.append("No clearly extractable final answer statement.")
        correctness_decision_reason = "Final-answer marker or usable last line was not found."
        if expected_answer is None:
            correctness_feedback = "Final answer missing and expected answer unavailable; correctness cannot be verified."
            correctness_evidence_missing.append("Expected answer not provided for verification.")
            correctness_decision_reason = "Missing final answer plus missing expected answer blocks correctness verification."
    else:
        correctness_evidence_found.append(f"Extracted final answer: {extracted_final}")
        if expected_answer is None:
            correctness = min(correctness, 2)
            correctness_feedback = "Expected answer missing; correctness could not be fully verified."
            correctness_evidence_missing.append("Expected answer not provided for verification.")
            correctness_decision_reason = "Correctness is partially assessed without expected answer."
        else:
            exact_match = _normalize(extracted_final) == _normalize(expected_answer)
            symbolic_validation = validate_final_answer(extracted_final, expected_answer)
            if exact_match or symbolic_validation["status"] == "equivalent":
                correctness_evidence_found.append(f"Matches expected answer: {expected_answer}")
                if not exact_match:
                    correctness_evidence_found.append("Symbolic equivalence validated by SymPy helper.")
                    correctness_decision_reason = (
                        "Final answer accepted by symbolic equivalence while rubric remains source of truth."
                    )
            else:
                correctness = 1
                correctness_errors.append("incomplete_final_answer")
                correctness_feedback = "Final answer is not correct even though work may contain useful steps."
                correctness_evidence_missing.append(f"Expected answer mismatch against: {expected_answer}")
                correctness_decision_reason = "Extracted final answer does not match expected answer."
                if symbolic_validation["status"] == "parse_error":
                    correctness_evidence_missing.append("Symbolic validation parse error reduced certainty.")
    correctness_verifiable = expected_answer is not None and bool(extracted_final)

    if conceptual_misunderstanding:
        correctness = min(correctness, 1)
        correctness_errors.append("concept_gap")
        correctness_feedback = "The response shows conceptual misunderstanding of core ideas."
        correctness_evidence_found.append("Conceptual misunderstanding pattern detected.")
        correctness_decision_reason = "Concept-level misconception overrides correctness confidence."

    criterion_results.append(
        CriterionResult(
            criterion="correctness",
            max_score=4,
            awarded_score=correctness,
            lost_marks=4 - correctness,
            error_types=sorted(set(correctness_errors)),
            feedback=correctness_feedback,
            evidence_found=correctness_evidence_found,
            evidence_missing=correctness_evidence_missing,
            decision_reason=correctness_decision_reason,
        )
    )

    method = 3 if has_method else 1
    method_errors = [] if has_method else ["method_gap"]
    method_feedback = "Method steps are present and follow a valid process." if has_method else "Method is incomplete or not visible."
    method_evidence_found = ["Detected method/process tokens."] if has_method else []
    method_evidence_missing = [] if has_method else ["No strong method tokens detected."]
    method_decision_reason = (
        "Method criterion awarded from visible procedural steps."
        if has_method
        else "Method criterion reduced due to missing procedural signals."
    )
    if conceptual_misunderstanding:
        method = min(method, 1)
        method_errors = sorted(set(method_errors + ["concept_gap"]))
        method_feedback = "Method reflects a concept-level misunderstanding."
        method_evidence_found.append("Conceptual misunderstanding pattern detected.")
        method_decision_reason = "Concept-level misconception caps method marks."

    criterion_results.append(
        CriterionResult(
            criterion="method",
            max_score=3,
            awarded_score=method,
            lost_marks=3 - method,
            error_types=method_errors,
            feedback=method_feedback,
            evidence_found=method_evidence_found,
            evidence_missing=method_evidence_missing,
            decision_reason=method_decision_reason,
        )
    )

    reasoning = 2 if has_reasoning else 0
    reasoning_errors = [] if has_reasoning else ["missing_reasoning"]
    reasoning_feedback = "Reasoning is explicit and understandable." if has_reasoning else "Reasoning is missing."
    reasoning_evidence_found = ["Reasoning connector tokens detected."] if has_reasoning else []
    reasoning_evidence_missing = [] if has_reasoning else ["No explicit reasoning connectors found."]
    reasoning_decision_reason = (
        "Reasoning marks awarded from explicit explanation language."
        if has_reasoning
        else "Reasoning marks lost because explanation language is absent."
    )
    criterion_results.append(
        CriterionResult(
            criterion="reasoning",
            max_score=2,
            awarded_score=reasoning,
            lost_marks=2 - reasoning,
            error_types=reasoning_errors,
            feedback=reasoning_feedback,
            evidence_found=reasoning_evidence_found,
            evidence_missing=reasoning_evidence_missing,
            decision_reason=reasoning_decision_reason,
        )
    )

    clarity = 1
    clarity_errors: List[str] = []
    clarity_feedback = "Working is clear."
    clarity_evidence_found = ["No unclear markers detected; length appears adequate."]
    clarity_evidence_missing: List[str] = []
    clarity_decision_reason = "Clarity marks awarded due to readable and sufficiently long working."
    if unclear or len(text) < MIN_SOLUTION_LENGTH:
        clarity = 0
        clarity_errors.append("unclear_working")
        clarity_feedback = "Working is unclear or too brief to verify."
        clarity_evidence_found = []
        if unclear:
            clarity_evidence_missing.append("Unclear token(s) detected in working.")
        if len(text) < MIN_SOLUTION_LENGTH:
            clarity_evidence_missing.append("Solution length below minimum threshold.")
        clarity_decision_reason = "Clarity marks removed due to unclear or too-short working."

    criterion_results.append(
        CriterionResult(
            criterion="clarity",
            max_score=1,
            awarded_score=clarity,
            lost_marks=1 - clarity,
            error_types=clarity_errors,
            feedback=clarity_feedback,
            evidence_found=clarity_evidence_found,
            evidence_missing=clarity_evidence_missing,
            decision_reason=clarity_decision_reason,
        )
    )

    total_score = sum(c.awarded_score for c in criterion_results)
    max_score = sum(c.max_score for c in criterion_results)
    lost_marks = max_score - total_score
    percentage = round((total_score / max_score) * 100, 2) if max_score else 0.0

    all_errors_raw = {e for c in criterion_results for e in c.error_types}
    unknown_error_types = sorted(e for e in all_errors_raw if e not in ERROR_DNA_CATEGORIES)
    if unknown_error_types:
        raise RuntimeError(
            f"Unsupported error types generated in criterion assessment: {', '.join(unknown_error_types)}"
        )
    all_errors = sorted(all_errors_raw)
    evidence_strength = total_score / max_score if max_score else 0.0
    confidence_result = assess_confidence(
        solution_text=text,
        confirmed_by_student=solution_input.confirmed_by_student,
        evidence_strength=evidence_strength,
        error_types=all_errors,
        expected_answer_available=expected_answer is not None,
        correctness_verifiable=correctness_verifiable,
    )
    if symbolic_validation and symbolic_validation["status"] == "parse_error":
        confidence_result["confidence"] = "low"
        confidence_result["teacher_review_needed"] = True
        reasons = confidence_result.get("reasons", [])
        if "symbolic_parse_error" not in reasons:
            reasons.append("symbolic_parse_error")
        confidence_result["reasons"] = reasons

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
        awarded_marks=total_score,
        total_marks=max_score,
        percentage=percentage,
        total_score=total_score,
        max_score=max_score,
        lost_marks=lost_marks,
        error_types=all_errors,
        feedback_summary=feedback_summary,
        rewrite_guidance=rewrite_guidance,
        confidence=confidence_result["confidence"],
        teacher_review_needed=bool(confidence_result["teacher_review_needed"]),
        symbolic_validation=symbolic_validation,
    )
    return result.to_dict()

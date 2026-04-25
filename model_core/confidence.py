from typing import Dict, List, Optional

from .models import MIN_SOLUTION_LENGTH


def assess_confidence(
    solution_text: str,
    confirmed_by_student: bool,
    evidence_strength: float,
    error_types: Optional[List[str]] = None,
    expected_answer_available: bool = True,
    correctness_verifiable: bool = True,
) -> Dict[str, object]:
    text = (solution_text or "").strip()
    lowered = text.lower()
    reasons: List[str] = []

    if not confirmed_by_student:
        reasons.append("solution_unconfirmed")

    if len(text) < MIN_SOLUTION_LENGTH:
        reasons.append("too_short")

    unclear_tokens = ["???", "idk", "not sure", "unclear", "..."]
    if any(token in lowered for token in unclear_tokens):
        reasons.append("unclear_working")

    if evidence_strength < 0.5:
        reasons.append("weak_evidence")

    if not expected_answer_available and not correctness_verifiable:
        reasons.append("correctness_unverified")

    if error_types and "unclear_working" in error_types and "unclear_working" not in reasons:
        reasons.append("unclear_working")

    low_triggers = {"solution_unconfirmed", "too_short", "unclear_working", "weak_evidence", "correctness_unverified"}
    is_low = any(r in low_triggers for r in reasons)

    if is_low:
        confidence = "low"
    elif evidence_strength < 0.75:
        confidence = "medium"
    else:
        confidence = "high"

    return {
        "confidence": confidence,
        "teacher_review_needed": (
            confidence == "low"
            or "solution_unconfirmed" in reasons
            or "too_short" in reasons
            or "unclear_working" in reasons
            or "correctness_unverified" in reasons
        ),
        "reasons": reasons,
    }

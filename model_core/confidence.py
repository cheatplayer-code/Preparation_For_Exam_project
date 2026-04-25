from typing import Dict, List, Optional


def assess_confidence(
    solution_text: str,
    confirmed_by_student: bool,
    evidence_strength: float,
    error_types: Optional[List[str]] = None,
) -> Dict[str, object]:
    text = (solution_text or "").strip()
    lowered = text.lower()
    reasons: List[str] = []

    if not confirmed_by_student:
        reasons.append("solution_unconfirmed")

    if len(text) < 20:
        reasons.append("too_short")

    unclear_tokens = ["???", "idk", "not sure", "unclear", "..."]
    if any(token in lowered for token in unclear_tokens):
        reasons.append("unclear_working")

    if evidence_strength < 0.5:
        reasons.append("weak_evidence")

    if error_types and "unclear_working" in error_types and "unclear_working" not in reasons:
        reasons.append("unclear_working")

    low_triggers = {"solution_unconfirmed", "too_short", "unclear_working", "weak_evidence"}
    is_low = any(r in low_triggers for r in reasons)

    if is_low:
        confidence = "low"
    elif evidence_strength < 0.75:
        confidence = "medium"
    else:
        confidence = "high"

    return {
        "confidence": confidence,
        "teacher_review_needed": confidence == "low",
        "reasons": reasons,
    }

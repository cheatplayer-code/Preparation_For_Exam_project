from typing import Dict, Union

from .models import ERROR_DNA_CATEGORIES, ErrorDNAProfile


CATEGORY_WEIGHTS = {
    "concept_gap": 0.30,
    "method_gap": 0.20,
    "algebra_error": 0.20,
    "missing_reasoning": 0.15,
    "notation_issue": 0.10,
    "misread_question": 0.25,
    "incomplete_final_answer": 0.12,
    "language_misinterpretation": 0.20,
    "unclear_working": 0.12,
    "time_management": 0.08,
}


def _default_weaknesses() -> Dict[str, float]:
    return {category: 0.0 for category in ERROR_DNA_CATEGORIES}


def update_error_dna(
    student_id: str,
    marking_result: Dict[str, object],
    current_profile: Union[ErrorDNAProfile, Dict[str, object], None] = None,
) -> Dict[str, object]:
    if isinstance(current_profile, ErrorDNAProfile):
        weaknesses = dict(current_profile.weaknesses)
    elif isinstance(current_profile, dict):
        weaknesses = dict(current_profile.get("weaknesses", {}))
    else:
        weaknesses = {}

    merged = _default_weaknesses()
    merged.update({k: float(v) for k, v in weaknesses.items() if k in merged})

    total_lost = float(marking_result.get("lost_marks", 0) or 0)
    max_score = float(marking_result.get("max_score", 1) or 1)
    severity_multiplier = 1.0 + (total_lost / max_score)

    for err in marking_result.get("error_types", []):
        if err in merged:
            merged[err] = round(min(1.0, merged[err] + CATEGORY_WEIGHTS.get(err, 0.1) * severity_multiplier), 4)

    profile = ErrorDNAProfile(student_id=student_id, weaknesses=merged)
    return profile.to_dict()

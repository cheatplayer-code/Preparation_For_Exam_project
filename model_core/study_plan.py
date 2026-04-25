from typing import Dict, List

from .models import ERROR_DNA_CATEGORIES

DEFAULT_FOCUS_CATEGORIES = ["method_gap", "missing_reasoning", "time_management"]


def generate_7_day_plan(error_dna_profile: Dict[str, object]) -> Dict[str, object]:
    student_id = error_dna_profile.get("student_id", "unknown_student")
    weaknesses = error_dna_profile.get("weaknesses", {}) or {}

    normalized = {cat: float(weaknesses.get(cat, 0.0)) for cat in ERROR_DNA_CATEGORIES}
    ranked = sorted(normalized.items(), key=lambda kv: kv[1], reverse=True)

    top_focus = [cat for cat, score in ranked if score > 0][:3]
    if len(top_focus) < 3:
        for default_cat in DEFAULT_FOCUS_CATEGORIES:
            if default_cat not in top_focus:
                top_focus.append(default_cat)
            if len(top_focus) == 3:
                break

    days: List[Dict[str, object]] = []
    for i in range(7):
        focus = top_focus[i % len(top_focus)]
        days.append(
            {
                "day": i + 1,
                "focus_error_category": focus,
                "objective": f"Reduce {focus.replace('_', ' ')} through guided practice.",
                "tasks": [
                    "Review one solved example and label each step.",
                    "Solve two targeted problems and self-check against rubric.",
                    "Write a short reflection on mistakes and corrections.",
                ],
            }
        )

    return {
        "student_id": student_id,
        "plan_type": "7_day_recovery",
        "days": days,
    }

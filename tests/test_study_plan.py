from model_core.study_plan import generate_7_day_plan


def test_generate_7_day_plan_structure():
    profile = {
        "student_id": "stu_002",
        "weaknesses": {
            "concept_gap": 0.8,
            "method_gap": 0.6,
            "missing_reasoning": 0.5,
        },
    }
    plan = generate_7_day_plan(profile)
    assert plan["student_id"] == "stu_002"
    assert len(plan["days"]) == 7
    assert all("focus_error_category" in day for day in plan["days"])

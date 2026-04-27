import pytest

from evals.synthetic_v04_cases import SYNTHETIC_SOLUTIONS
from model_core.rubric_engine import mark_solution


@pytest.mark.parametrize("case", SYNTHETIC_SOLUTIONS, ids=[case["case_id"] for case in SYNTHETIC_SOLUTIONS])
def test_synthetic_solutions_stability(case):
    data = {
        "solution_text": case["solution_text"],
        "student_id": case["case_id"],
        "question_id": case["case_id"],
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": case["confirmed_by_student"],
        "input_source": case["input_source"],
    }
    result = mark_solution(data, expected_answer=case["expected_answer"])

    assert result["awarded_marks"] == case["expected_awarded_marks"]
    assert sorted(result["error_types"]) == sorted(case["expected_error_types"])
    assert result["confidence"] == case["expected_confidence"]
    assert result["teacher_review_needed"] == case["expected_teacher_review_needed"]

import pytest

from model_core.rubric_engine import mark_solution


SYNTHETIC_SOLUTIONS = [
    {
        "case_id": "synthetic_01_fully_correct",
        "solution_text": "I form the equation and simplify step by step because both sides match. final answer: x = 4",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_02_missing_reasoning",
        "solution_text": "equation simplify isolate x. final answer: x = 4",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 8,
        "expected_error_types": ["missing_reasoning"],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_03_wrong_final_answer",
        "solution_text": "I write equation and simplify because this isolates x. final answer: x = 5",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "medium",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_04_concept_gap",
        "solution_text": "I solve by saying triangle has four sides so the equation works. final answer: 9",
        "expected_answer": "6",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 3,
        "expected_error_types": ["concept_gap", "incomplete_final_answer", "missing_reasoning"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_05_unclear_and_short",
        "solution_text": "idk ???",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 2,
        "expected_error_types": ["incomplete_final_answer", "method_gap", "missing_reasoning", "unclear_working"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_06_unconfirmed_submission",
        "solution_text": "I form equation and simplify. final answer: x=4",
        "expected_answer": "x=4",
        "confirmed_by_student": False,
        "input_source": "manual_edit",
        "expected_awarded_marks": 8,
        "expected_error_types": ["missing_reasoning"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_07_missing_expected_answer",
        "solution_text": "I form the equation and simplify each side, and isolate x. therefore x = 4",
        "expected_answer": None,
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 8,
        "expected_error_types": [],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_08_symbolic_equivalence",
        "solution_text": "I simplify and solve because both expressions match. final answer: x^2 - 1",
        "expected_answer": "(x - 1)(x + 1)",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_09_symbolic_equivalent_missing_reasoning",
        "solution_text": "equation simplify isolate. final answer: x^2 - 1",
        "expected_answer": "(x - 1)(x + 1)",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 8,
        "expected_error_types": ["missing_reasoning"],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_10_ocr_draft_clean_solution",
        "solution_text": "I solve and show each step because this is valid and clear. final answer: y=2",
        "expected_answer": "y=2",
        "confirmed_by_student": True,
        "input_source": "ocr_draft",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_11_too_short_submission",
        "solution_text": "I solved",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 4,
        "expected_error_types": ["incomplete_final_answer", "missing_reasoning", "unclear_working"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_12_numeric_equivalence",
        "solution_text": "I substitute values and simplify because the method is correct. answer: 3/4",
        "expected_answer": "0.75",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
]


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
    assert result["error_types"] == case["expected_error_types"]
    assert result["confidence"] == case["expected_confidence"]
    assert result["teacher_review_needed"] is case["expected_teacher_review_needed"]

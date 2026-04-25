import json

import pytest

from model_core.models import ERROR_DNA_CATEGORIES
from model_core.rubric_engine import mark_solution


def test_fully_correct_solution():
    data = {
        "solution_text": "I form the equation, simplify each side, and isolate x. Because both sides are equal, final answer: x = 4",
        "student_id": "s1",
        "question_id": "q1",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="x=4")
    assert result["total_score"] == result["max_score"]
    assert result["error_types"] == []
    assert result["teacher_review_needed"] is False


def test_correct_answer_missing_reasoning():
    data = {
        "solution_text": "equation simplify isolate x. final answer: x = 4",
        "student_id": "s2",
        "question_id": "q2",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="x=4")
    assert "missing_reasoning" in result["error_types"]


def test_wrong_final_answer_but_correct_method():
    data = {
        "solution_text": "I write the equation and simplify step by step because this isolates x. final answer: x = 5",
        "student_id": "s3",
        "question_id": "q3",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="x=4")
    assert "incomplete_final_answer" in result["error_types"]
    method = next((c for c in result["criterion_results"] if c["criterion"] == "method"), None)
    assert method is not None
    assert method["awarded_score"] >= 2


def test_conceptual_misunderstanding():
    data = {
        "solution_text": "I solve by saying triangle has four sides so the equation works. final answer: 9",
        "student_id": "s4",
        "question_id": "q4",
        "topic": "geometry",
        "subskill": "triangle",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="6")
    assert "concept_gap" in result["error_types"]


def test_unconfirmed_solution_low_confidence():
    data = {
        "solution_text": "I form equation and simplify. final answer: x=4",
        "student_id": "s5",
        "question_id": "q5",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": False,
        "input_source": "manual_edit",
    }
    result = mark_solution(data, expected_answer="x=4")
    assert result["confidence"] == "low"
    assert result["teacher_review_needed"] is True


def test_unclear_solution_triggers_teacher_review_needed():
    data = {
        "solution_text": "idk ???",
        "student_id": "s6",
        "question_id": "q6",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="x=4")
    assert "unclear_working" in result["error_types"]
    assert result["teacher_review_needed"] is True


def test_invalid_input_source_raises_validation_error():
    data = {
        "solution_text": "I solve and therefore final answer: x = 4",
        "student_id": "s7",
        "question_id": "q7",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "invalid_source",
    }
    with pytest.raises(ValueError, match="input_source"):
        mark_solution(data, expected_answer="x=4")


def test_empty_solution_raises_validation_error():
    data = {
        "solution_text": "   ",
        "student_id": "s8",
        "question_id": "q8",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    with pytest.raises(ValueError, match="solution_text"):
        mark_solution(data, expected_answer="x=4")


def test_all_error_types_are_from_allowed_taxonomy():
    data = {
        "solution_text": "idk ??? final answer: x = 5",
        "student_id": "s9",
        "question_id": "q9",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="x=4")
    allowed = set(ERROR_DNA_CATEGORIES)
    assert set(result["error_types"]).issubset(allowed)
    for criterion in result["criterion_results"]:
        assert set(criterion["error_types"]).issubset(allowed)


def test_missing_expected_answer_triggers_teacher_review():
    data = {
        "solution_text": "I form the equation, simplify each side, and isolate x. therefore x = 4",
        "student_id": "s10",
        "question_id": "q10",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer=None)
    assert result["teacher_review_needed"] is True


def test_criterion_trace_fields_are_present():
    data = {
        "solution_text": "I solve by equation and simplify because each step follows. final answer: x = 4",
        "student_id": "s11",
        "question_id": "q11",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="x=4")
    for criterion in result["criterion_results"]:
        assert "evidence_found" in criterion
        assert "evidence_missing" in criterion
        assert "decision_reason" in criterion
        assert isinstance(criterion["evidence_found"], list)
        assert isinstance(criterion["evidence_missing"], list)
        assert isinstance(criterion["decision_reason"], str)


def test_percentage_and_examiner_style_marks_fields():
    data = {
        "solution_text": "equation isolate x. final answer: x = 4",
        "student_id": "s12",
        "question_id": "q12",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="x=4")
    assert result["awarded_marks"] == result["total_score"]
    assert result["total_marks"] == result["max_score"]
    assert result["total_marks"] > 0
    expected_percentage = round((result["awarded_marks"] / result["total_marks"]) * 100, 2)
    assert result["percentage"] == expected_percentage


def test_output_is_json_serializable():
    data = {
        "solution_text": "I form equation and simplify because both sides are equal. final answer: x = 4",
        "student_id": "s13",
        "question_id": "q13",
        "topic": "algebra",
        "subskill": "linear",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="x=4")
    encoded = json.dumps(result)
    assert isinstance(encoded, str)


def test_rubric_output_includes_symbolic_validation_when_expected_answer_provided():
    data = {
        "solution_text": "I simplify and solve because both expressions match. final answer: x^2 - 1",
        "student_id": "s14",
        "question_id": "q14",
        "topic": "algebra",
        "subskill": "factorization",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="(x - 1)(x + 1)")
    assert "symbolic_validation" in result
    assert result["symbolic_validation"] is not None
    assert result["symbolic_validation"]["status"] == "equivalent"


def test_symbolic_validation_does_not_override_missing_reasoning_lost_marks():
    data = {
        "solution_text": "equation simplify isolate. final answer: x^2 - 1",
        "student_id": "s15",
        "question_id": "q15",
        "topic": "algebra",
        "subskill": "factorization",
        "confirmed_by_student": True,
        "input_source": "typed",
    }
    result = mark_solution(data, expected_answer="(x - 1)(x + 1)")
    assert result["symbolic_validation"]["status"] == "equivalent"
    assert "missing_reasoning" in result["error_types"]
    reasoning = next((c for c in result["criterion_results"] if c["criterion"] == "reasoning"), None)
    assert reasoning is not None
    assert reasoning["lost_marks"] > 0

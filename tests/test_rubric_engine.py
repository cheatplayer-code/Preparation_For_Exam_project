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
    method = next(c for c in result["criterion_results"] if c["criterion"] == "method")
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
        "input_source": "manual_ocr",
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

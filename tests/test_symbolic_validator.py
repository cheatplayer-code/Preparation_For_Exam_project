from model_core.symbolic_validator import MAX_SYMBOLIC_INPUT_LENGTH, validate_final_answer


def test_equivalent_factorization_identity():
    result = validate_final_answer("x^2 - 1", "(x - 1)(x + 1)")
    assert result["status"] == "equivalent"
    assert result["confidence_impact"] == "increase"
    assert result["teacher_review_recommended"] is False


def test_equivalent_distributive_identity():
    result = validate_final_answer("2*x + 2", "2*(x + 1)")
    assert result["status"] == "equivalent"


def test_not_equivalent_expression():
    result = validate_final_answer("x + 2", "x + 3")
    assert result["status"] == "not_equivalent"
    assert result["teacher_review_recommended"] is False


def test_parse_error_returns_teacher_review_recommended():
    result = validate_final_answer("x +", "x + 1")
    assert result["status"] == "parse_error"
    assert result["teacher_review_recommended"] is True


def test_missing_expected_answer_not_applicable():
    result = validate_final_answer("x + 1", "")
    assert result["status"] == "not_applicable"
    assert result["teacher_review_recommended"] is True


def test_empty_student_answer_returns_parse_error():
    result = validate_final_answer("", "x=4")
    assert result["status"] == "parse_error"
    assert result["teacher_review_recommended"] is True
    assert result["confidence_impact"] == "decrease"


def test_unsafe_expression_returns_parse_error():
    result = validate_final_answer("__import__('os')", "x=4")
    assert result["status"] == "parse_error"
    assert result["teacher_review_recommended"] is True


def test_too_long_expression_returns_parse_error():
    result = validate_final_answer("x" * (MAX_SYMBOLIC_INPUT_LENGTH + 1), "x=4")
    assert result["status"] == "parse_error"
    assert result["teacher_review_recommended"] is True


def test_same_equation_returns_equivalent():
    result = validate_final_answer("x=4", "x=4")
    assert result["status"] == "equivalent"


def test_equation_different_forms_not_equivalent_with_current_logic():
    result = validate_final_answer("2*x=8", "x=4")
    assert result["status"] != "equivalent"

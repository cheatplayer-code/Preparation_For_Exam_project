from model_core.symbolic_validator import validate_final_answer


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

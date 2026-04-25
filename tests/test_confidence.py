from model_core.confidence import assess_confidence


def test_assess_confidence_high():
    out = assess_confidence(
        solution_text="I solve step by step because this is valid and clearly justified.",
        confirmed_by_student=True,
        evidence_strength=0.9,
    )
    assert out["confidence"] == "high"
    assert out["teacher_review_needed"] is False


def test_assess_confidence_low_when_unconfirmed():
    out = assess_confidence(solution_text="Valid solution", confirmed_by_student=False, evidence_strength=0.9)
    assert out["confidence"] == "low"
    assert out["teacher_review_needed"] is True


def test_assess_confidence_low_when_correctness_unverified():
    out = assess_confidence(
        solution_text="I solved the equation and got x=4",
        confirmed_by_student=True,
        evidence_strength=0.9,
        expected_answer_available=False,
        correctness_verifiable=False,
    )
    assert out["confidence"] == "low"
    assert out["teacher_review_needed"] is True
    assert "correctness_unverified" in out["reasons"]

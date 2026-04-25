from model_core.error_dna import update_error_dna


def test_error_dna_updates_known_categories():
    marking = {
        "lost_marks": 4,
        "max_score": 10,
        "error_types": ["concept_gap", "missing_reasoning", "unclear_working"],
    }
    profile = update_error_dna("stu_001", marking)
    assert profile["student_id"] == "stu_001"
    assert profile["weaknesses"]["concept_gap"] > 0
    assert profile["weaknesses"]["missing_reasoning"] > 0
    assert profile["weaknesses"]["unclear_working"] > 0

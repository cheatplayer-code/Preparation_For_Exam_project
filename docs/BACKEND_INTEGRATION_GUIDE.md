# Backend Integration Guide

## Installation / import assumption
This is a Python package-style module. Backend services can import model-core functions directly.

## Public functions
- mark_solution(solution_input, expected_answer=None)
- validate_final_answer(student_answer, expected_answer)
- update_error_dna(student_id, marking_result, current_profile=None)
- generate_7_day_plan(error_dna_profile)

## Example: mark one solution
```python
from model_core.rubric_engine import mark_solution

solution_input = {
    "solution_text": "Expand and simplify: 2(x+3)=2x+6, so x=4.",
    "student_id": "student_001",
    "question_id": "question_001",
    "topic": "algebra",
    "subskill": "linear_equations",
    "confirmed_by_student": True,
    "input_source": "typed",
}

result = mark_solution(solution_input, expected_answer="x=4")
```

## Example: update Error DNA after marking
```python
from model_core.error_dna import update_error_dna

updated_profile = update_error_dna(
    student_id="student_001",
    marking_result=result,
    current_profile=None,
)
```

## Example: generate 7-day plan
```python
from model_core.study_plan import generate_7_day_plan

plan = generate_7_day_plan(updated_profile)
```

## Important integration rules
- confirmed_by_student must be boolean.
- input_source must be typed | manual_edit | ocr_draft.
- OCR text must be confirmed or edited by the student before trusted marking.
- Low confidence means teacher_review_needed should be surfaced in the UI.
- Symbolic validation is helper-only, not a full grader.
- Do not show outputs as official NIS/MESC scores.
- Do not claim official NIS affiliation.

## Expected output fields
- awarded_marks
- total_marks
- percentage
- criterion_results
- lost_marks
- error_types
- feedback_summary
- rewrite_guidance
- confidence
- teacher_review_needed
- symbolic_validation

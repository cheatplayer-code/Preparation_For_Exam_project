# INTEGRATION_CONTRACT

## Input contract for `mark_solution`
Dictionary with:
- solution_text: str (required, non-empty after trim)
- student_id: str (required)
- question_id: str (required)
- topic: str (required, non-empty after trim)
- subskill: str (required, non-empty after trim)
- confirmed_by_student: bool (required, must be boolean)
- input_source: str (required, one of: `typed`, `manual_edit`, `ocr_draft`)

Optional parameter:
- expected_answer: str | None

## Output contract from `mark_solution`
JSON-serializable dictionary with:
- student_id, question_id, topic, subskill
- criterion_results[]:
  - criterion
  - max_score
  - awarded_score
  - lost_marks
  - error_types[]
  - feedback
  - evidence_found[] (trace evidence supporting marks)
  - evidence_missing[] (trace evidence for lost marks/uncertainty)
  - decision_reason (criterion decision rationale)
- awarded_marks (examiner-style alias of `total_score`)
- total_marks (examiner-style alias of `max_score`)
- percentage (float, rounded to 2 dp, `awarded_marks / total_marks * 100`)
- total_score (backward-compatible)
- max_score (backward-compatible)
- lost_marks
- error_types[]
- feedback_summary
- rewrite_guidance
- confidence (`high|medium|low`)
- teacher_review_needed (bool)
- symbolic_validation (object | null, present when expected_answer is provided):
  - status (`equivalent|not_equivalent|parse_error|not_applicable`)
  - student_expression
  - expected_expression
  - normalized_student_expression
  - normalized_expected_expression
  - confidence_impact (`increase|decrease|neutral`)
  - teacher_review_recommended (bool)
  - reason

### `teacher_review_needed` trigger logic (v0.2)
`teacher_review_needed` is true if any of these hold:
- confidence is low
- solution is unconfirmed
- solution is too short
- unclear working is detected
- expected_answer is missing and correctness cannot be verified

### Symbolic validation helper scope (v0.3)
- SymPy is used only as a helper to check final-answer mathematical equivalence when possible.
- The rubric engine remains the source of truth for grading decisions.
- SymPy output does not grade reasoning, method quality, notation quality, or missing steps.

## Input contract for `update_error_dna`
- student_id: str
- marking_result: dict from `mark_solution`
- current_profile: optional existing profile dict

## Output contract from `update_error_dna`
- student_id
- weaknesses: map of all Error DNA categories to float in [0,1]

## Input contract for `generate_7_day_plan`
- error_dna_profile dict with `student_id` and `weaknesses`

## Output contract for `generate_7_day_plan`
- student_id
- plan_type
- days[7], each with:
  - day
  - focus_error_category
  - objective
  - tasks[]

# INTEGRATION_CONTRACT

## Input contract for `mark_solution`
Dictionary with:
- solution_text: str
- student_id: str
- question_id: str
- topic: str
- subskill: str
- confirmed_by_student: bool
- input_source: str (`typed` or manually confirmed OCR text source)

Optional parameter:
- expected_answer: str

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
- total_score
- max_score
- lost_marks
- error_types[]
- feedback_summary
- rewrite_guidance
- confidence (`high|medium|low`)
- teacher_review_needed (bool)

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

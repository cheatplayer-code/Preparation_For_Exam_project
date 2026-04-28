# Synthetic Stability Dataset – Coverage Notes (v0.7)

The synthetic stability dataset in `evals/synthetic_v04_cases.py` contains **25 cases**.
Each case exercises a specific model-core behaviour or edge condition.

## Case coverage map

| # | case_id | Primary behaviour tested |
|---|---------|--------------------------|
| 01 | synthetic_01_fully_correct | Fully correct solution (typed, confirmed) – baseline pass |
| 02 | synthetic_02_missing_reasoning | Correct answer and method, but no reasoning tokens |
| 03 | synthetic_03_wrong_final_answer | Wrong final answer with valid method and reasoning |
| 04 | synthetic_04_concept_gap | Conceptual misunderstanding overrides method and correctness |
| 05 | synthetic_05_unclear_and_short | Unclear tokens (`idk`, `???`) combined with short working |
| 06 | synthetic_06_unconfirmed_submission | `confirmed_by_student=False` forces low confidence |
| 07 | synthetic_07_missing_expected_answer | No expected answer supplied; correctness unverifiable |
| 08 | synthetic_08_symbolic_equivalence | `x^2 - 1` symbolically equivalent to `(x-1)(x+1)` |
| 09 | synthetic_09_symbolic_equivalent_missing_reasoning | Symbolic equivalence accepted but reasoning absent |
| 10 | synthetic_10_ocr_draft_clean_solution | `ocr_draft` source with confirmed, clean solution |
| 11 | synthetic_11_too_short_submission | Solution below `MIN_SOLUTION_LENGTH` threshold |
| 12 | synthetic_12_numeric_equivalence | `3/4` numerically equivalent to `0.75` |
| 13 | synthetic_13_correct_answer_no_method | Correct answer with reasoning but **no method tokens** |
| 14 | synthetic_14_correct_answer_no_reasoning_no_method | Correct answer, no reasoning, no method |
| 15 | synthetic_15_correct_method_missing_final_answer | Method and reasoning present but **no final answer declared** |
| 16 | synthetic_16_symbolic_parse_error_in_final_answer | Broken symbolic expression (`sin((x`) triggers parse_error |
| 17 | synthetic_17_unsafe_symbolic_input_in_final_answer | Unsafe characters in final answer (`@#$`) trigger parse_error |
| 18 | synthetic_18_equation_limitation_2x_eq_8 | `2*x=8` is not yet recognised as equivalent to `x=4` (known limitation) |
| 19 | synthetic_19_notation_issue_reversed_equation | Reversed equation `4=x` not recognised as equivalent to `x=4` |
| 20 | synthetic_20_misread_question_marker | Wrong answer from correct method; surfaces misread-question pattern |
| 21 | synthetic_21_language_misinterpretation_marker | Systematic wrong answer from misinterpreted phrasing |
| 22 | synthetic_22_time_management_marker | Correct working begun but no final answer; time-management scenario |
| 23 | synthetic_23_multiple_error_types | Five concurrent errors: concept_gap, method_gap, missing_reasoning, unclear_working, incomplete_final_answer |
| 24 | synthetic_24_ocr_draft_unconfirmed | `ocr_draft` + `confirmed_by_student=False` → low confidence despite perfect working |
| 25 | synthetic_25_manual_edit_clean_confirmed | `manual_edit` + `confirmed_by_student=True` + fully correct → high confidence |

## Future-facing cases

Cases 18–22 represent behaviours that the **current deterministic rubric does not yet
detect explicitly**.  They are included as stability anchors that document the current
(conservative) model output.  Each case carries a `TODO` comment in the source explaining
what a future rubric version should detect:

| Case | Category not yet detected | Planned improvement |
|------|---------------------------|---------------------|
| 18 | `algebra_error` (equation equivalence) | Solve-based equation comparison in `symbolic_validator` |
| 19 | `notation_issue` (reversed equation) | Side-order normalisation in `symbolic_validator` |
| 20 | `misread_question` | Heuristic or metadata flag to detect systematic mis-reading |
| 21 | `language_misinterpretation` | Language-level signal distinct from simple wrong-answer |
| 22 | `time_management` | Detect absent final answer after complete working as time_management |

## Error DNA taxonomy used

All error types emitted by the rubric are drawn from `ERROR_DNA_CATEGORIES` in
`model_core/models.py`:

- `concept_gap`
- `method_gap`
- `algebra_error`
- `missing_reasoning`
- `notation_issue`
- `misread_question`
- `incomplete_final_answer`
- `language_misinterpretation`
- `unclear_working`
- `time_management`

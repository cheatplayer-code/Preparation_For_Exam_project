# Model-Core Quality Report (v1.0)

## Summary
- synthetic stability eval: 25/25 passed
- Error DNA eval: 5/5 passed
- combined eval: overall passed
- total failures: 0
- pytest: 66 passed

## Synthetic evaluation summary
Synthetic evaluation: 25/25 passed (100.0%), avg_marks=7.20, teacher_review_rate=40.0%

## Error DNA evaluation summary
Error DNA evaluation: 5/5 passed (100.0%)

## What the evals prove
- The 25-case synthetic stability dataset passes without regressions.
- Error DNA aggregation and 7-day plan focus categories are consistent across synthetic histories.
- Confidence and teacher-review flags remain stable under combined evaluation runs.
- The combined eval runner reports overall pass status with zero failures.

## What the evals do NOT prove
- Real student performance or classroom validity.
- Full rubric correctness for all curricula or question types.
- Official NIS/MESC alignment or scoring endorsement.
- OCR or LLM-based interpretation quality.

## Known limitations
- rubric engine is still deterministic/keyword-based
- no OCR yet
- no real LLM yet
- no official NIS exam validation
- symbolic equation solving is limited
- future-facing categories like notation_issue/misread_question/language_misinterpretation/time_management are not deeply detected yet

## Recommended next version after v1.0
v1.1 demo runner or v1.1 backend handoff package

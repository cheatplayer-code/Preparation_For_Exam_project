# Error DNA Evaluation Notes — v0.8

## Why student-level evaluation matters

The model-core is not only a single-attempt marker. Its broader purpose is to build a
**student weakness profile over time** using the Error DNA system. A student may submit
many attempts across different questions and sessions; the Error DNA profile accumulates
evidence of recurring error patterns, and the 7-day study plan is then derived from those
accumulated weaknesses.

v0.6 added a synthetic stability eval that checks single-attempt marking correctness.
v0.7 expanded the single-attempt dataset to 25 cases.

v0.8 closes the gap by evaluating **multi-attempt Error DNA aggregation**: given a sequence
of attempts (each referencing an existing synthetic case), does the resulting Error DNA
profile and study-plan correctly reflect the student's repeated error patterns?

---

## The 5 synthetic student profiles

### 1. `reasoning_gap_student`
Attempts: synthetic_02, synthetic_09, synthetic_14.
All three cases produce `missing_reasoning`. After three attempts the `missing_reasoning`
weakness score dominates the profile, and the 7-day plan focuses on it.

### 2. `final_answer_accuracy_student`
Attempts: synthetic_03, synthetic_15, synthetic_18, synthetic_19.
All four cases surface `incomplete_final_answer`. After four attempts the
`incomplete_final_answer` score is the highest in the profile.

### 3. `low_confidence_unclear_student`
Attempts: synthetic_05, synthetic_16, synthetic_17, synthetic_22, synthetic_06.
These cases combine unclear tokens, symbolic parse errors, unsafe input characters,
time-management markers, and an unconfirmed submission. Every attempt triggers
`teacher_review_needed=True` (count = 5). The accumulated profile shows
`incomplete_final_answer` and `unclear_working` as prominent weaknesses.

### 4. `concept_gap_student`
Attempts: synthetic_04, synthetic_23.
Both cases include a conceptual misunderstanding pattern, which carries the highest
category weight (0.30). After two attempts `concept_gap` is capped at 1.0 and is the
dominant weakness. Both attempts require teacher review (count = 2).

### 5. `mixed_errors_student`
Attempts: synthetic_02, synthetic_04, synthetic_13, synthetic_05.
Covers four different error categories: `missing_reasoning`, `concept_gap`,
`method_gap`, and `unclear_working`. The final profile has at least two significant
weaknesses; the 7-day plan focuses on the top accumulated categories.

---

## Why contains-style checks are used instead of exact equality

Exact equality on Error DNA profiles or study plans would make the eval fragile:

- **Category weight tuning**: if CATEGORY_WEIGHTS are adjusted in the future, scores
  change but the ordering of the top weaknesses should remain stable.
- **Plan ordering**: `generate_7_day_plan` cycles through the top three weaknesses.
  Minor score re-ordering could change which category lands on which day without
  changing the overall set of focus areas.
- **Default padding**: the plan pads up to three focus categories using
  `DEFAULT_FOCUS_CATEGORIES`. The padding categories may change without affecting
  whether the student's real weaknesses appear.

The eval therefore checks only that:
1. `teacher_review_needed_count` matches exactly (this is a deterministic count, not
   a score, so it should always be stable).
2. Every `expected_top_weaknesses` item appears somewhere in `top_weaknesses`
   (the full ranked list of categories with score > 0).
3. Every `expected_plan_focus_contains` item appears in the set of
   `plan_focus_categories` (unique focus categories across the 7-day plan).

This keeps the eval meaningful while tolerating future weight and ordering adjustments.

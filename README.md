# Preparation_For_Exam_project

This repository currently contains the **model-core package only** for MESC Lab.

## Scope
- Student solution input handling
- Deterministic rubric-based marking
- Error DNA profile updates
- 7-day study plan generation
- Confidence and teacher-review flags

## Out of Scope
- Frontend
- Backend API/endpoints
- Database
- OCR integration
- LLM integration

## Backend imports
```python
from model_core.rubric_engine import mark_solution
from model_core.error_dna import update_error_dna
from model_core.study_plan import generate_7_day_plan
```

## Running synthetic evaluation
```bash
python3 -m evals.run_synthetic_eval
python3 -m evals.run_synthetic_eval --json-only
```

## v0.6 evaluation report options
```bash
python3 -m evals.run_synthetic_eval
python3 -m evals.run_synthetic_eval --json-only
python3 -m evals.run_synthetic_eval --summary-only
python3 -m evals.run_synthetic_eval --output eval_reports/latest_synthetic_eval.json
python3 -m evals.run_synthetic_eval --markdown-output eval_reports/latest_synthetic_eval.md
python3 -m evals.run_synthetic_eval --fail-on-regression
```

## v0.7 synthetic stability dataset

The synthetic stability dataset now contains **25 cases** (up from 12 in v0.6).

The new cases cover: correct answer without visible method, correct answer without
reasoning or method, correct method without a final answer, symbolic parse errors,
unsafe symbolic input, the equation-equivalence limitation (`2*x=8` vs `x=4`),
notation issues, misread-question patterns, language misinterpretation, time management,
multi-error submissions, OCR-draft unconfirmed solutions, and clean manual-edit confirmed
solutions.

v0.7 expands the synthetic stability dataset to cover more edge cases. Some categories
are represented as future-facing cases when the current deterministic rubric does not yet
detect them explicitly.

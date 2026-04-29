# Preparation_For_Exam_project

This repository currently contains the **model-core package only** for MESC Lab.

## v1.0 Stable Model-Core Freeze
- Stable, integration-ready model-core behavior for rubric marking, symbolic final-answer validation helper, confidence + teacher review logic, Error DNA aggregation, 7-day study plan generation, and synthetic evaluation runners.
- Public import functions:
```python
from model_core.rubric_engine import mark_solution
from model_core.error_dna import update_error_dna
from model_core.study_plan import generate_7_day_plan
from model_core.symbolic_validator import validate_final_answer
```
- Run all evals:
```bash
python3 -m evals.run_all_evals --summary-only
python3 -m evals.run_all_evals --fail-on-regression
```
- Documentation: VERSION.md, CHANGELOG.md, docs/BACKEND_INTEGRATION_GUIDE.md, docs/MODEL_CORE_QUALITY_REPORT.md

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
from model_core.symbolic_validator import validate_final_answer
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

## v0.8 Error DNA evaluation

v0.8 adds multi-attempt Error DNA aggregation evaluation. The eval runner simulates five
synthetic student histories (repeated attempts), accumulates Error DNA profiles across
attempts, and verifies that the resulting weakness profiles and 7-day study plans contain
the expected focus categories.

```bash
python3 -m evals.run_error_dna_eval
python3 -m evals.run_error_dna_eval --json-only
python3 -m evals.run_error_dna_eval --summary-only
python3 -m evals.run_error_dna_eval --output eval_reports/latest_error_dna_eval.json
python3 -m evals.run_error_dna_eval --fail-on-regression
```

## v0.9 combined evaluation runner

v0.9 adds a combined runner that executes both the synthetic stability eval and the Error DNA
eval in a single command and returns a unified report with `overall_passed` and `total_failures`.

```bash
python3 -m evals.run_all_evals
python3 -m evals.run_all_evals --json-only
python3 -m evals.run_all_evals --summary-only
python3 -m evals.run_all_evals --output eval_reports/latest_all_evals.json
python3 -m evals.run_all_evals --fail-on-regression
```

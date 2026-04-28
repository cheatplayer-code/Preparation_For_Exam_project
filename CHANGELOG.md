# CHANGELOG

All notable changes to the **model-core** package are documented here.

---

## v1.0.0 — Stable model-core freeze

- Froze the model-core as the first stable, integration-ready release.
- Added `VERSION.md`, `CHANGELOG.md`, `docs/BACKEND_INTEGRATION_GUIDE.md`, and
  `docs/MODEL_CORE_QUALITY_REPORT.md`.
- Added `__version__ = "1.0.0"` to `model_core/__init__.py`.
- Added `tests/test_version_v10.py` to assert the version string.
- No scoring logic, synthetic case expected outputs, or Error DNA evaluation
  expectations were changed.

---

## v0.9 — Combined eval runner

- Added `evals/run_all_evals.py` to execute both the synthetic stability eval and
  the Error DNA eval in a single command.
- Unified report includes `overall_passed` and `total_failures`.

---

## v0.8 — Error DNA student-history eval

- Added `evals/run_error_dna_eval.py` and `evals/student_histories_v08.py`.
- Simulates five synthetic student histories with repeated attempts; accumulates
  Error DNA profiles across attempts and verifies expected weakness categories
  and 7-day study plan focus areas.

---

## v0.7 — Expanded 25-case synthetic dataset

- Expanded synthetic stability dataset from 12 to 25 cases in
  `evals/synthetic_v04_cases.py`.
- New cases cover: correct answer without visible method, correct answer without
  reasoning, correct method without a final answer, symbolic parse errors, unsafe
  symbolic input, equation-equivalence limitation, notation issues, misread-question
  patterns, language misinterpretation, time management, multi-error submissions,
  OCR-draft unconfirmed solutions, and clean manual-edit confirmed solutions.

---

## v0.6 — Saved reports + failure categories

- Extended `evals/run_synthetic_eval.py` with `--output` (JSON), `--markdown-output`,
  `--summary-only`, `--json-only`, and `--fail-on-regression` options.
- Eval reports can now be persisted to `eval_reports/`.

---

## v0.5 — Synthetic eval runner

- Added `evals/run_synthetic_eval.py` as the first automated evaluation runner for
  the synthetic stability dataset.

---

## v0.4 — Synthetic stability dataset

- Introduced `evals/synthetic_v04_cases.py` with the initial 12-case synthetic
  stability dataset used to regression-test scoring behaviour.

---

## v0.3.1 — Symbolic safety hardening

- Hardened `symbolic_validator` against unsafe SymPy expressions (e.g. very large
  exponents, `__import__`, wildcard inputs).
- Added additional test coverage in `tests/test_symbolic_validator.py`.

---

## v0.3 — SymPy symbolic helper

- Added `model_core/symbolic_validator.py` providing `validate_final_answer()` as a
  helper for checking algebraic equivalence of student answers via SymPy.

---

## v0.2 — Validation + traceability

- Added `confirmed_by_student` and `input_source` fields to solution input.
- Introduced `teacher_review_needed` and `confidence` flags in marking output.
- Improved per-criterion traceability in `criterion_results`.

---

## v0.1 — Initial scaffold

- Initial scaffold of `model_core` with `rubric_engine`, `error_dna`, `study_plan`,
  `confidence`, and `models` modules.
- Basic deterministic keyword-based rubric marking.
- Error DNA profile aggregation across student attempts.
- 7-day study plan generation from an Error DNA profile.

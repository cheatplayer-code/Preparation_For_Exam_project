# RUBRIC_MODEL

Deterministic rubric criteria:
- correctness (0-4)
- method (0-3)
- reasoning (0-2)
- clarity (0-1)

Output includes:
- criterion-level scores
- lost marks
- error types
- feedback summary
- rewrite guidance
- confidence
- teacher_review_needed
- symbolic_validation (when expected answer is provided)

No OCR and no LLM are used.

## SymPy helper boundary (v0.3)
- SymPy validates final-answer equivalence only.
- It does not grade reasoning quality, method steps, notation quality, or exam-style explanation.
- Rubric scoring remains the authoritative grading engine.

## v0.3.1 symbolic validation hardening
- Symbolic validation performs safe input checks before SymPy parsing.
- Empty, unsafe, or too-long expressions return `parse_error` and recommend teacher review.
- Equation support is limited to expression-form comparison and is not full solution-set equivalence checking.
- Full solve-based equation equivalence is planned for a future version.
- Rubric engine remains the authoritative grading layer.

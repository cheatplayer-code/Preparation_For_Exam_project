# Student Demo Guide (v1.1)

## Purpose of the demo
Provide a deterministic, end-to-end walkthrough of the model-core pipeline using a single demo student and four synthetic attempts. This is intended for presentations and backend handoff validation.

## Command examples
```bash
python3 -m demo.run_student_demo
python3 -m demo.run_student_demo --summary-only
python3 -m demo.run_student_demo --json-only
python3 -m demo.run_student_demo --output demo_reports/latest_student_demo.json
```

## What the demo proves
- The model-core pipeline runs end-to-end: marking → Error DNA updates → 7-day plan generation.
- Output is deterministic and JSON-serializable.
- Confidence, teacher-review flags, and feedback fields surface consistently for each attempt.

## What the demo does not prove
- No frontend, backend API, database, OCR, or LLM integration.
- No change to scoring logic or synthetic case expectations.
- No real-world exam validity beyond the existing synthetic cases.

## How backend/frontend teams can use this reference flow
- Mirror the request/response shape for `mark_solution`, `update_error_dna`, and `generate_7_day_plan`.
- Use the demo JSON output as a sample payload for UI mocks and API contracts.
- Validate that orchestration wiring matches the pipeline demonstrated here before connecting real services.

# MODEL_SPEC

## Scope
This repository contains only model-core logic for MESC Lab:
- student solution input handling
- deterministic rubric marking
- error DNA update
- 7-day study plan generation
- confidence + teacher review flagging

Out of scope:
- frontend
- backend API/routes
- database
- OCR integration
- LLM integration

## Package
`model_core/`

## Main imports for backend integration
```python
from model_core.rubric_engine import mark_solution
from model_core.error_dna import update_error_dna
from model_core.study_plan import generate_7_day_plan
```

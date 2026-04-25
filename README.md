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

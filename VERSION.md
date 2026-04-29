# VERSION

Current version: v1.3.0
Version status: CI-enabled model-core package

Scope:
- rubric marking
- symbolic final-answer validation helper
- confidence + teacher review logic
- Error DNA aggregation
- 7-day study plan generation
- synthetic evaluation runners

Explicitly out of scope:
- frontend
- backend API
- database
- OCR
- real LLM
- official NIS/MESC integration

Compatibility promise:
Public import functions should remain stable unless a future major version changes them.

Public import functions:
```python
from model_core.rubric_engine import mark_solution
from model_core.error_dna import update_error_dna
from model_core.study_plan import generate_7_day_plan
from model_core.symbolic_validator import validate_final_answer
```

v1.3 notes:
- GitHub Actions CI workflow for model-core
- pytest coverage in CI
- combined eval regression checks in CI
- student demo smoke test in CI
- console script smoke tests in CI

# VERSION

## Current Version: v1.0.0

**Status:** Stable model-core freeze

## Scope

This version covers the following model-core components:

- Rubric marking (`rubric_engine`)
- Symbolic final-answer validation helper (`symbolic_validator`)
- Confidence + teacher review logic (`confidence`)
- Error DNA aggregation (`error_dna`)
- 7-day study plan generation (`study_plan`)
- Synthetic evaluation runners (`evals/`)

## Explicitly Out of Scope

The following are **not** part of this package and are not provided here:

- Frontend
- Backend API / endpoints
- Database
- OCR integration
- Real LLM integration
- Official NIS/MESC integration

## Compatibility Promise

The following public import functions are considered **stable** and will remain
backward-compatible unless a future **major version** explicitly changes them:

```python
from model_core.rubric_engine import mark_solution
from model_core.error_dna import update_error_dna
from model_core.study_plan import generate_7_day_plan
from model_core.symbolic_validator import validate_final_answer
```

Any breaking change to these function signatures or return-value contracts will
require a new major version (e.g. v2.0).

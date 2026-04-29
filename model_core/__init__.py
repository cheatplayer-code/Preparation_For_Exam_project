"""Model-core package for deterministic assessment and planning."""

from .rubric_engine import mark_solution
from .error_dna import update_error_dna
from .study_plan import generate_7_day_plan

__version__ = "1.3.0"

__all__ = ["mark_solution", "update_error_dna", "generate_7_day_plan", "__version__"]

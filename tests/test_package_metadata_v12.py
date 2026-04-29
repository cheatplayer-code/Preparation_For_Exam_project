from pathlib import Path

import model_core
from model_core import generate_7_day_plan, mark_solution, update_error_dna
from model_core.symbolic_validator import validate_final_answer


def test_package_public_imports_and_version():
    assert model_core.__version__ == "1.2.0"
    assert mark_solution
    assert update_error_dna
    assert generate_7_day_plan
    assert validate_final_answer


def test_pyproject_metadata():
    repo_root = Path(__file__).resolve().parents[1]
    pyproject_path = repo_root / "pyproject.toml"
    assert pyproject_path.exists()
    assert 'name = "mesc-lab-model-core"' in pyproject_path.read_text()

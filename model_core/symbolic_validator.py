from typing import Dict
import re

from sympy import simplify
from sympy.core.sympify import SympifyError
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)
MAX_SYMBOLIC_INPUT_LENGTH = 300
SAFE_SYMBOLIC_PATTERN = r"^[0-9a-zA-Z_+\-*/^().=,\s]+$"
_SAFE_SYMBOLIC_RE = re.compile(SAFE_SYMBOLIC_PATTERN)


def _to_comparable_expression(raw: str) -> str:
    expr = (raw or "").strip()
    if "=" in expr:
        # Current behavior compares equations by expression form, not by solution-set equivalence.
        # TODO: add solve-based equation comparison in a future version.
        left, right = expr.split("=", 1)
        return f"({left.strip()})-({right.strip()})"
    return expr


def validate_final_answer(student_answer: str, expected_answer: str) -> Dict[str, object]:
    student_expression = (student_answer or "").strip()
    expected_expression = (expected_answer or "").strip()

    result: Dict[str, object] = {
        "status": "not_applicable",
        "student_expression": student_expression,
        "expected_expression": expected_expression,
        "normalized_student_expression": "",
        "normalized_expected_expression": "",
        "confidence_impact": "decrease",
        "teacher_review_recommended": True,
        "reason": "Expected answer is missing.",
    }

    if not expected_expression:
        return result

    if not student_expression:
        result.update(
            {
                "status": "parse_error",
                "confidence_impact": "decrease",
                "teacher_review_recommended": True,
                "reason": "Student answer is missing.",
            }
        )
        return result

    if (
        len(student_expression) > MAX_SYMBOLIC_INPUT_LENGTH
        or len(expected_expression) > MAX_SYMBOLIC_INPUT_LENGTH
    ):
        result.update(
            {
                "status": "parse_error",
                "confidence_impact": "decrease",
                "teacher_review_recommended": True,
                "reason": f"Expression exceeds maximum length limit of {MAX_SYMBOLIC_INPUT_LENGTH} characters.",
            }
        )
        return result

    if not _SAFE_SYMBOLIC_RE.fullmatch(student_expression) or not _SAFE_SYMBOLIC_RE.fullmatch(expected_expression):
        result.update(
            {
                "status": "parse_error",
                "confidence_impact": "decrease",
                "teacher_review_recommended": True,
                "reason": "Expression contains unsafe characters.",
            }
        )
        return result

    try:
        student_expr = parse_expr(
            _to_comparable_expression(student_expression),
            transformations=_TRANSFORMATIONS,
            evaluate=True,
        )
        expected_expr = parse_expr(
            _to_comparable_expression(expected_expression),
            transformations=_TRANSFORMATIONS,
            evaluate=True,
        )
    except (SympifyError, SyntaxError, TypeError, ValueError):
        result.update(
            {
                "status": "parse_error",
                "confidence_impact": "decrease",
                "teacher_review_recommended": True,
                "reason": "Could not parse one or both expressions for symbolic comparison.",
            }
        )
        return result

    normalized_student = str(simplify(student_expr))
    normalized_expected = str(simplify(expected_expr))
    result["normalized_student_expression"] = normalized_student
    result["normalized_expected_expression"] = normalized_expected

    try:
        equivalent = bool(simplify(student_expr - expected_expr) == 0)
    except (TypeError, ValueError, NotImplementedError):
        equivalent = normalized_student == normalized_expected

    if equivalent:
        result.update(
            {
                "status": "equivalent",
                "confidence_impact": "increase",
                "teacher_review_recommended": False,
                "reason": "Expressions are symbolically equivalent.",
            }
        )
    else:
        result.update(
            {
                "status": "not_equivalent",
                "confidence_impact": "neutral",
                "teacher_review_recommended": False,
                "reason": "Expressions are not symbolically equivalent.",
            }
        )

    return result

from typing import Dict

from sympy import simplify
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)


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

    try:
        student_expr = parse_expr(student_expression, transformations=_TRANSFORMATIONS, evaluate=True)
        expected_expr = parse_expr(expected_expression, transformations=_TRANSFORMATIONS, evaluate=True)
    except Exception:
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
    except Exception:
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

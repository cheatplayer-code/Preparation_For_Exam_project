# Synthetic student histories for v0.8 Error DNA evaluation.
#
# Each history references existing case_ids from synthetic_v04_cases.py.
# Expected values were derived by tracing update_error_dna accumulation across
# the listed attempts and then inspecting generate_7_day_plan output.

STUDENT_HISTORIES = [
    {
        "student_id": "reasoning_gap_student",
        "description": (
            "Student consistently omits reasoning connectors across three attempts. "
            "All three cases carry missing_reasoning; two also share method_gap."
        ),
        "attempts": [
            "synthetic_02_missing_reasoning",
            "synthetic_09_symbolic_equivalent_missing_reasoning",
            "synthetic_14_correct_answer_no_reasoning_no_method",
        ],
        "expected_top_weaknesses": ["missing_reasoning"],
        "expected_teacher_review_needed_count": 0,
        "expected_plan_focus_contains": ["missing_reasoning"],
    },
    {
        "student_id": "final_answer_accuracy_student",
        "description": (
            "Student repeatedly submits an incorrect or missing final answer. "
            "Four distinct cases all surface incomplete_final_answer."
        ),
        "attempts": [
            "synthetic_03_wrong_final_answer",
            "synthetic_15_correct_method_missing_final_answer",
            "synthetic_18_equation_limitation_2x_eq_8",
            "synthetic_19_notation_issue_reversed_equation",
        ],
        "expected_top_weaknesses": ["incomplete_final_answer"],
        "expected_teacher_review_needed_count": 0,
        "expected_plan_focus_contains": ["incomplete_final_answer"],
    },
    {
        "student_id": "low_confidence_unclear_student",
        "description": (
            "Student accumulates unclear, unsafe-symbol, parse-error, and unconfirmed "
            "submissions. All five attempts require teacher review."
        ),
        "attempts": [
            "synthetic_05_unclear_and_short",
            "synthetic_16_symbolic_parse_error_in_final_answer",
            "synthetic_17_unsafe_symbolic_input_in_final_answer",
            "synthetic_22_time_management_marker",
            "synthetic_06_unconfirmed_submission",
        ],
        "expected_top_weaknesses": ["unclear_working", "incomplete_final_answer"],
        "expected_teacher_review_needed_count": 5,
        "expected_plan_focus_contains": ["incomplete_final_answer"],
    },
    {
        "student_id": "concept_gap_student",
        "description": (
            "Student shows persistent conceptual misunderstanding in both attempts. "
            "concept_gap weight (0.30) dominates the Error DNA profile."
        ),
        "attempts": [
            "synthetic_04_concept_gap",
            "synthetic_23_multiple_error_types",
        ],
        "expected_top_weaknesses": ["concept_gap"],
        "expected_teacher_review_needed_count": 2,
        "expected_plan_focus_contains": ["concept_gap"],
    },
    {
        "student_id": "mixed_errors_student",
        "description": (
            "Student exhibits a spread of error categories: missing_reasoning, "
            "concept_gap, method_gap, and unclear_working across four attempts."
        ),
        "attempts": [
            "synthetic_02_missing_reasoning",
            "synthetic_04_concept_gap",
            "synthetic_13_correct_answer_no_method",
            "synthetic_05_unclear_and_short",
        ],
        "expected_top_weaknesses": ["missing_reasoning", "method_gap"],
        "expected_teacher_review_needed_count": 2,
        "expected_plan_focus_contains": ["missing_reasoning", "method_gap"],
    },
]

SYNTHETIC_SOLUTIONS = [
    {
        "case_id": "synthetic_01_fully_correct",
        "solution_text": "I form the equation and simplify step by step because both sides match. final answer: x = 4",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_02_missing_reasoning",
        "solution_text": "equation simplify isolate x. final answer: x = 4",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 8,
        "expected_error_types": ["missing_reasoning"],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_03_wrong_final_answer",
        "solution_text": "I write equation and simplify because this isolates x. final answer: x = 5",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "medium",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_04_concept_gap",
        "solution_text": "I solve by saying triangle has four sides so the equation works. final answer: 9",
        "expected_answer": "6",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 3,
        "expected_error_types": ["concept_gap", "incomplete_final_answer", "missing_reasoning"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_05_unclear_and_short",
        "solution_text": "idk ???",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 2,
        "expected_error_types": ["incomplete_final_answer", "method_gap", "missing_reasoning", "unclear_working"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_06_unconfirmed_submission",
        "solution_text": "I form equation and simplify. final answer: x=4",
        "expected_answer": "x=4",
        "confirmed_by_student": False,
        "input_source": "manual_edit",
        "expected_awarded_marks": 8,
        "expected_error_types": ["missing_reasoning"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_07_missing_expected_answer",
        "solution_text": "I form the equation and simplify each side, and isolate x. therefore x = 4",
        "expected_answer": None,
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 8,
        "expected_error_types": [],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_08_symbolic_equivalence",
        "solution_text": "I simplify and solve because both expressions match. final answer: x^2 - 1",
        "expected_answer": "(x - 1)(x + 1)",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_09_symbolic_equivalent_missing_reasoning",
        "solution_text": "equation simplify isolate. final answer: x^2 - 1",
        "expected_answer": "(x - 1)(x + 1)",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 8,
        "expected_error_types": ["missing_reasoning"],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_10_ocr_draft_clean_solution",
        "solution_text": "I solve and show each step because this is valid and clear. final answer: y=2",
        "expected_answer": "y=2",
        "confirmed_by_student": True,
        "input_source": "ocr_draft",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        "case_id": "synthetic_11_too_short_submission",
        "solution_text": "I solved",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 4,
        "expected_error_types": ["incomplete_final_answer", "missing_reasoning", "unclear_working"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        "case_id": "synthetic_12_numeric_equivalence",
        "solution_text": "I substitute values and simplify because the method is correct. answer: 3/4",
        "expected_answer": "0.75",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    # --- v0.7 additions: cases 13–25 ---
    {
        # Correct final answer but no visible method (no method-token words).
        # TODO: future rubric version should reward partial credit for "correct answer without method"
        # as a distinct pattern rather than only penalizing method_gap.
        "case_id": "synthetic_13_correct_answer_no_method",
        "solution_text": "I recall the answer because it matches what I studied. final answer: x = 4",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 8,
        "expected_error_types": ["method_gap"],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
    {
        # Correct final answer but no reasoning and no method tokens.
        # TODO: future rubric could distinguish "bare-answer" submissions as their own category.
        "case_id": "synthetic_14_correct_answer_no_reasoning_no_method",
        "solution_text": "x equals four. final answer: x = 4",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 6,
        "expected_error_types": ["method_gap", "missing_reasoning"],
        "expected_confidence": "medium",
        "expected_teacher_review_needed": False,
    },
    {
        # Correct method and reasoning present, but no explicit final answer declared.
        # The rubric falls back to the last line, which is not the expected answer.
        # TODO: future rubric could detect "working present, answer absent" as incomplete_final_answer
        # without requiring the last-line heuristic to accidentally match.
        "case_id": "synthetic_15_correct_method_missing_final_answer",
        "solution_text": "I solve by isolating x then simplify each side because the algebra is valid.\nNo final answer stated.",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "medium",
        "expected_teacher_review_needed": False,
    },
    {
        # Final answer contains a syntactically broken symbolic expression (unmatched parenthesis).
        # The symbolic validator returns parse_error, which forces confidence to low and
        # triggers teacher review.
        "case_id": "synthetic_16_symbolic_parse_error_in_final_answer",
        "solution_text": "I simplify the equation and solve because the method is correct. final answer: sin((x",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        # Final answer contains characters outside the safe symbolic whitelist (@, #, $).
        # The symbolic validator returns parse_error (unsafe chars), forcing low confidence.
        "case_id": "synthetic_17_unsafe_symbolic_input_in_final_answer",
        "solution_text": "I substitute values and simplify because the formula is valid. final answer: x = @#$",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        # Equation limitation: student correctly writes 2*x=8 which is equivalent to x=4,
        # but the current symbolic validator compares (2*x-8) vs (x-4) and finds them
        # not equivalent.
        # TODO: future symbolic_validator should use solve-based comparison for equations
        # so that 2*x=8 is recognised as equivalent to x=4.
        "case_id": "synthetic_18_equation_limitation_2x_eq_8",
        "solution_text": "I form the equation and solve because this is the standard method. final answer: 2*x=8",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "medium",
        "expected_teacher_review_needed": False,
    },
    {
        # Notation issue: student writes "4 = x" instead of "x = 4".
        # The current rubric does not normalise equation side-order, so it marks this wrong.
        # TODO: future rubric should detect reversed-equation notation as notation_issue
        # rather than incomplete_final_answer.
        "case_id": "synthetic_19_notation_issue_reversed_equation",
        "solution_text": "I solve by isolating x and simplify because this makes the algebra clear. final answer: 4 = x",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "medium",
        "expected_teacher_review_needed": False,
    },
    {
        # Misread question: student has correct method and reasoning but answers a different
        # question (x=7 instead of x=4).  Current rubric cannot detect misread_question
        # from solution text alone; it surfaces as incomplete_final_answer.
        # TODO: future rubric version should tag misread_question when the method is sound
        # but the final answer reflects a systematic mis-reading of the problem.
        "case_id": "synthetic_20_misread_question_marker",
        "solution_text": "I form the equation and simplify each step because I read the question carefully. final answer: x = 7",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "medium",
        "expected_teacher_review_needed": False,
    },
    {
        # Language misinterpretation: student interprets and solves with correct procedure
        # but misunderstands the meaning and arrives at x=2.  Current rubric cannot detect
        # language_misinterpretation; it surfaces as incomplete_final_answer.
        # TODO: future rubric should detect language_misinterpretation as a distinct category.
        "case_id": "synthetic_21_language_misinterpretation_marker",
        "solution_text": "I interpret the question and solve by substituting values because the formula applies. final answer: x = 2",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "medium",
        "expected_teacher_review_needed": False,
    },
    {
        # Time management: student begins with correct method and reasoning but does not
        # complete the solution (no final answer stated).  Current rubric cannot detect
        # time_management; it surfaces as incomplete_final_answer via the last-line fallback.
        # The fallback sentence is passed to the symbolic validator which returns parse_error,
        # forcing confidence to low and requiring teacher review.
        # TODO: future rubric should detect time_management when working is present but
        # the final answer is absent.
        "case_id": "synthetic_22_time_management_marker",
        "solution_text": "I start forming the equation and begin to isolate x step by step but have no time to finish.",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 7,
        "expected_error_types": ["incomplete_final_answer"],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        # Multiple error types in a single submission: unclear token, conceptual
        # misunderstanding, wrong answer, no method, no reasoning.
        "case_id": "synthetic_23_multiple_error_types",
        "solution_text": "idk. The triangle has four sides. final answer: 9",
        "expected_answer": "6",
        "confirmed_by_student": True,
        "input_source": "typed",
        "expected_awarded_marks": 2,
        "expected_error_types": [
            "concept_gap",
            "incomplete_final_answer",
            "method_gap",
            "missing_reasoning",
            "unclear_working",
        ],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        # OCR-draft source, solution unconfirmed by student.
        # Even a fully correct, well-reasoned solution gets confidence=low and
        # teacher_review_needed=True because confirmed_by_student is False.
        "case_id": "synthetic_24_ocr_draft_unconfirmed",
        "solution_text": "I solve the equation and simplify each step because this method is correct. final answer: x = 4",
        "expected_answer": "x=4",
        "confirmed_by_student": False,
        "input_source": "ocr_draft",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "low",
        "expected_teacher_review_needed": True,
    },
    {
        # Manual-edit source, confirmed by student, fully correct and well-reasoned.
        # Tests that manual_edit input_source with confirmed=True behaves identically
        # to typed when the solution is clean.
        "case_id": "synthetic_25_manual_edit_clean_confirmed",
        "solution_text": "I form the equation, then substitute values, and simplify each step because the algebra is valid. final answer: x = 4",
        "expected_answer": "x=4",
        "confirmed_by_student": True,
        "input_source": "manual_edit",
        "expected_awarded_marks": 10,
        "expected_error_types": [],
        "expected_confidence": "high",
        "expected_teacher_review_needed": False,
    },
]


import json

from .error_dna import update_error_dna
from .rubric_engine import mark_solution
from .study_plan import generate_7_day_plan


def run_demo() -> None:
    sample_input = {
        "solution_text": "I form an equation and simplify. Because both sides balance, final answer: x = 4",
        "student_id": "stu_001",
        "question_id": "q_101",
        "topic": "algebra",
        "subskill": "linear_equations",
        "confirmed_by_student": True,
        "input_source": "typed",
    }

    marking = mark_solution(sample_input, expected_answer="x=4")
    dna = update_error_dna(student_id=sample_input["student_id"], marking_result=marking)
    plan = generate_7_day_plan(dna)

    payload = {"marking": marking, "error_dna": dna, "study_plan": plan}
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    run_demo()

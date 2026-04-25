from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

MIN_SOLUTION_LENGTH = 20
ALLOWED_INPUT_SOURCES = ["typed", "manual_edit", "ocr_draft"]


ERROR_DNA_CATEGORIES = [
    "concept_gap",
    "method_gap",
    "algebra_error",
    "missing_reasoning",
    "notation_issue",
    "misread_question",
    "incomplete_final_answer",
    "language_misinterpretation",
    "unclear_working",
    "time_management",
]


@dataclass
class StudentSolutionInput:
    solution_text: str
    student_id: str
    question_id: str
    topic: str
    subskill: str
    confirmed_by_student: bool
    input_source: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CriterionResult:
    criterion: str
    max_score: int
    awarded_score: int
    lost_marks: int
    error_types: List[str] = field(default_factory=list)
    feedback: str = ""
    evidence_found: List[str] = field(default_factory=list)
    evidence_missing: List[str] = field(default_factory=list)
    decision_reason: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MarkingResult:
    student_id: str
    question_id: str
    topic: str
    subskill: str
    criterion_results: List[CriterionResult]
    awarded_marks: int
    total_marks: int
    percentage: float
    total_score: int
    max_score: int
    lost_marks: int
    error_types: List[str]
    feedback_summary: str
    rewrite_guidance: str
    confidence: str
    teacher_review_needed: bool
    symbolic_validation: Optional[Dict[str, object]] = None

    def to_dict(self) -> Dict:
        data = asdict(self)
        data["criterion_results"] = [c.to_dict() for c in self.criterion_results]
        return data


@dataclass
class ErrorDNAProfile:
    student_id: str
    weaknesses: Dict[str, float]

    def to_dict(self) -> Dict:
        return asdict(self)

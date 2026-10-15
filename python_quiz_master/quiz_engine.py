"""GUI independent quiz flow and scoring logic."""
from __future__ import annotations

from dataclasses import dataclass
from random import Random
from time import monotonic
from typing import Sequence

from .question_bank import Question


@dataclass
class QuizAnswer:
    question: Question
    selected: str | None = None

    @property
    def is_correct(self) -> bool:
        return self.selected == self.question.answer


@dataclass(frozen=True)
class QuizSummary:
    total: int
    correct: int
    incorrect: int
    unanswered: int
    score: int
    percentage: float
    duration_seconds: int


class QuizSession:
    """Track a quiz session; each question can be answered only once."""

    def __init__(self, questions: Sequence[Question], *, shuffle: bool = True,
                 seed: int | None = None) -> None:
        if not questions:
            raise ValueError("A quiz must contain at least one question.")
        self.questions = list(questions)
        if shuffle:
            Random(seed).shuffle(self.questions)
        self.answers = [QuizAnswer(q) for q in self.questions]
        self.index = 0
        self.started_at = monotonic()

    @property
    def current(self) -> QuizAnswer:
        return self.answers[self.index]

    @property
    def finished(self) -> bool:
        return self.index >= len(self.answers)

    def submit(self, selected: str | None) -> bool:
        if self.finished:
            return False
        current = self.current
        if current.selected is not None:
            return False
        if selected is not None and selected not in current.question.options:
            raise ValueError("Selected answer is not one of the available options.")
        current.selected = selected
        return True

    def advance(self) -> bool:
        if self.finished:
            return False
        if self.current.selected is None:
            self.current.selected = ""
        self.index += 1
        return not self.finished

    def summary(self, duration_seconds: int | None = None) -> QuizSummary:
        correct = sum(a.is_correct for a in self.answers)
        unanswered = sum(a.selected is None or a.selected == "" for a in self.answers)
        incorrect = len(self.answers) - correct - unanswered
        duration = max(0, int(monotonic() - self.started_at)) if duration_seconds is None else max(0, duration_seconds)
        return QuizSummary(len(self.answers), correct, incorrect, unanswered,
                           correct, correct / len(self.answers) * 100, duration)


def performance_message(percentage: float) -> str:
    if percentage >= 90:
        return "Outstanding work!"
    if percentage >= 70:
        return "Great job! Keep it up."
    if percentage >= 50:
        return "Good effort. A little more practice will help."
    return "Keep practicing. Every attempt helps you improve."

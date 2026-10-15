"""Tests for GUI independent quiz scoring and flow."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from python_quiz_master.question_bank import QUESTIONS
from python_quiz_master.quiz_engine import QuizSession, performance_message


class QuizEngineTests(unittest.TestCase):
    def setUp(self):
        self.session = QuizSession(QUESTIONS[:2], shuffle=False)

    def test_correct_and_incorrect_scoring(self):
        self.session.submit(self.session.current.question.answer)
        self.session.advance()
        incorrect = next(option for option in self.session.current.question.options
                         if option != self.session.current.question.answer)
        self.session.submit(incorrect)
        summary = self.session.summary(8)
        self.assertEqual(summary.correct, 1)
        self.assertEqual(summary.incorrect, 1)
        self.assertEqual(summary.score, 1)
        self.assertEqual(summary.percentage, 50)

    def test_unanswered_and_expiration_advance(self):
        self.session.advance()
        self.assertEqual(self.session.index, 1)
        self.session.advance()
        self.assertTrue(self.session.finished)
        summary = self.session.summary(0)
        self.assertEqual(summary.unanswered, 2)
        self.assertEqual(summary.incorrect, 0)
        self.assertGreaterEqual(summary.duration_seconds, 0)

    def test_submit_only_once_and_validate_option(self):
        self.assertTrue(self.session.submit(self.session.current.question.options[0]))
        self.assertFalse(self.session.submit(self.session.current.question.answer))
        with self.assertRaises(ValueError):
            other = QuizSession(QUESTIONS[:1], shuffle=False)
            other.submit("absent")

    def test_empty_quiz_rejected_and_performance_message(self):
        with self.assertRaises(ValueError):
            QuizSession([])
        self.assertIn("Outstanding", performance_message(100))


if __name__ == "__main__":
    unittest.main()

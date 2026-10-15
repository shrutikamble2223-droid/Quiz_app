"""Tests for SQLite result and settings persistence."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from python_quiz_master.database import Database, DEFAULT_SETTINGS
from python_quiz_master.quiz_engine import QuizSession
from python_quiz_master.question_bank import QUESTIONS


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp.name) / "test.sqlite3")

    def tearDown(self):
        self.temp.cleanup()

    def test_initialization_and_result_round_trip(self):
        session = QuizSession(QUESTIONS[:1], shuffle=False)
        session.submit(session.current.question.answer)
        session.advance()
        summary = session.summary(12)
        review = [{"question": session.answers[0].question.prompt}]
        result_id = self.database.save_result("Alex", "Python Programming", "Easy", summary, review)
        result = self.database.get_result(result_id)
        self.assertEqual(result["player_name"], "Alex")
        self.assertEqual(result["correct"], 1)
        self.assertEqual(self.database.get_results()[0]["id"], result_id)

    def test_settings_persist_and_history_clear(self):
        settings = self.database.get_settings()
        self.assertEqual(settings["questions_per_quiz"], DEFAULT_SETTINGS["questions_per_quiz"])
        settings["timer_enabled"] = False
        self.database.save_settings(settings)
        self.assertFalse(self.database.get_settings()["timer_enabled"])
        self.database.clear_results()
        self.assertEqual(self.database.get_results(), [])


if __name__ == "__main__":
    unittest.main()

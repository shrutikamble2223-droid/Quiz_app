"""Launch Python Quiz Master."""
from __future__ import annotations

import json
import tkinter as tk
from tkinter import messagebox, ttk

from .database import DEFAULT_SETTINGS, Database
from .question_bank import CATEGORIES, DIFFICULTIES, QUESTIONS
from .quiz_engine import QuizSession, performance_message


class QuizApp(tk.Tk):
    """Single-window Tkinter quiz application."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Python Quiz Master")
        self.geometry("900x700")
        self.minsize(700, 560)
        self.database = Database()
        self.settings = self.database.get_settings()
        self.player = ""
        self.category = CATEGORIES[0]
        self.difficulty = DIFFICULTIES[0]
        self.session: QuizSession | None = None
        self.quiz_started = 0.0
        self.timer_remaining = 0
        self.timer_job: str | None = None
        self.result_id: int | None = None
        self._apply_theme()
        self.show_home()

    def _apply_theme(self) -> None:
        dark = bool(self.settings.get("dark_mode"))
        self.bg = "#172033" if dark else "#f3f6fb"
        self.surface = "#222d43" if dark else "#ffffff"
        self.fg = "#edf2fa" if dark else "#1e293b"
        self.muted = "#a8b4c7" if dark else "#64748b"
        self.accent = "#5875e8"
        self.configure(bg=self.bg)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.bg)
        style.configure("Card.TFrame", background=self.surface)
        style.configure("TLabel", background=self.bg, foreground=self.fg, font=("Segoe UI", 11))
        style.configure("Card.TLabel", background=self.surface, foreground=self.fg, font=("Segoe UI", 11))
        style.configure("Muted.TLabel", background=self.bg, foreground=self.muted, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.bg, foreground=self.fg, font=("Segoe UI", 25, "bold"))
        style.configure("Heading.TLabel", background=self.bg, foreground=self.fg, font=("Segoe UI", 17, "bold"))
        style.configure("TButton", font=("Segoe UI", 11), padding=(14, 9))
        style.configure("Accent.TButton", background=self.accent, foreground="white", font=("Segoe UI", 11, "bold"))
        style.map("Accent.TButton", background=[("active", "#405fd5")])
        style.configure("TCombobox", padding=7)
        style.configure("Horizontal.TProgressbar", troughcolor=self.surface, background=self.accent)
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _clear(self) -> ttk.Frame:
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        for child in self.winfo_children():
            child.destroy()
        container = ttk.Frame(self, padding=(38, 30))
        container.pack(fill="both", expand=True)
        return container

    def _header(self, parent: ttk.Frame, title: str, subtitle: str = "") -> None:
        ttk.Label(parent, text=title, style="Title.TLabel").pack(anchor="w", pady=(0, 5))
        if subtitle:
            ttk.Label(parent, text=subtitle, style="Muted.TLabel").pack(anchor="w", pady=(0, 20))

    def show_home(self) -> None:
        root = self._clear()
        self._header(root, "Python Quiz Master", "Choose a topic, challenge yourself, and track your progress.")
        card = ttk.Frame(root, style="Card.TFrame", padding=26)
        card.pack(fill="both", expand=True, pady=8)
        card.columnconfigure(1, weight=1)
        ttk.Label(card, text="Ready for a quiz?", style="Card.TLabel",
                  font=("Segoe UI", 17, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))
        ttk.Label(card, text="Your name", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=7)
        self.name_var = tk.StringVar(value=self.player)
        ttk.Entry(card, textvariable=self.name_var, font=("Segoe UI", 11)).grid(row=1, column=1, sticky="ew", padx=(16, 0), pady=7)
        ttk.Label(card, text="Category", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=7)
        self.category_var = tk.StringVar(value=self.category)
        ttk.Combobox(card, textvariable=self.category_var, values=CATEGORIES, state="readonly").grid(row=2, column=1, sticky="ew", padx=(16, 0), pady=7)
        ttk.Label(card, text="Difficulty", style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=7)
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        ttk.Combobox(card, textvariable=self.difficulty_var, values=DIFFICULTIES, state="readonly").grid(row=3, column=1, sticky="ew", padx=(16, 0), pady=7)
        actions = ttk.Frame(card, style="Card.TFrame")
        actions.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(23, 0))
        ttk.Button(actions, text="Start Quiz", style="Accent.TButton", command=self.start_quiz).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="View Results", command=self.show_history).pack(side="left", padx=8)
        ttk.Button(actions, text="Settings", command=self.show_settings).pack(side="left", padx=8)
        ttk.Button(actions, text="Exit", command=self.destroy).pack(side="right")
        count = len([q for q in QUESTIONS if q.category == self.category_var.get()])
        ttk.Label(root, text=f"{len(QUESTIONS)} sample questions across {len(CATEGORIES)} categories · {count} questions in this category",
                  style="Muted.TLabel").pack(anchor="w", pady=(8, 0))

    def start_quiz(self) -> None:
        player = self.name_var.get().strip()
        if not player:
            messagebox.showinfo("Name required", "Enter your name before starting the quiz.", parent=self)
            return
        if len(player) > 60:
            messagebox.showerror("Name too long", "Please use a name of 60 characters or fewer.", parent=self)
            return
        self.player = player
        self.category = self.category_var.get()
        self.difficulty = self.difficulty_var.get()
        pool = [q for q in QUESTIONS if q.category == self.category and q.difficulty == self.difficulty]
        if not pool:
            messagebox.showerror("No questions", "There are no questions for this selection.", parent=self)
            return
        amount = min(max(1, int(self.settings["questions_per_quiz"])), len(pool))
        import random
        self.session = QuizSession(random.sample(pool, amount), shuffle=True)
        self.quiz_started = __import__("time").monotonic()
        self._show_question()

    def _show_question(self) -> None:
        assert self.session is not None
        root = self._clear()
        answer = self.session.current
        q = answer.question
        root.columnconfigure(0, weight=1)
        ttk.Label(root, text=f"{self.category}  ·  {self.difficulty}", style="Muted.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(root, text=f"Question {self.session.index + 1} of {len(self.session.answers)}", style="Heading.TLabel").grid(row=1, column=0, sticky="w", pady=(10, 10))
        progress = ttk.Progressbar(root, maximum=len(self.session.answers), value=self.session.index, mode="determinate")
        progress.grid(row=2, column=0, sticky="ew", pady=(0, 24))
        card = ttk.Frame(root, style="Card.TFrame", padding=24)
        card.grid(row=3, column=0, sticky="nsew")
        root.rowconfigure(3, weight=1)
        ttk.Label(card, text=q.prompt, style="Card.TLabel", wraplength=740,
                  font=("Segoe UI", 16, "bold")).pack(anchor="w", fill="x", pady=(0, 20))
        self.choice_var = tk.StringVar(value="")
        self.answer_buttons: list[ttk.Radiobutton] = []
        options = list(q.options)
        __import__("random").shuffle(options)
        for i, option in enumerate(options, 1):
            button = ttk.Radiobutton(card, text=option, value=option, variable=self.choice_var)
            button.pack(anchor="w", fill="x", pady=7)
            self.answer_buttons.append(button)
        footer = ttk.Frame(root)
        footer.grid(row=4, column=0, sticky="ew", pady=(20, 0))
        self.timer_label = ttk.Label(footer, text="", style="Muted.TLabel")
        self.timer_label.pack(side="left")
        self.next_button = ttk.Button(footer, text="Next Question →", style="Accent.TButton", command=self._next_question)
        self.next_button.pack(side="right")
        if self.settings.get("timer_enabled"):
            self.timer_remaining = max(1, int(self.settings.get("timer_seconds", 20)))
            self._tick_timer()

    def _tick_timer(self) -> None:
        self.timer_label.configure(text=f"Time left: {self.timer_remaining}s")
        if self.timer_remaining <= 0:
            self._next_question(timeout=True)
            return
        self.timer_remaining -= 1
        self.timer_job = self.after(1000, self._tick_timer)

    def _next_question(self, timeout: bool = False) -> None:
        assert self.session is not None
        selected = None if timeout else self.choice_var.get() or None
        if selected is None and not timeout and not messagebox.askyesno("Skip question?", "Continue without selecting an answer?", parent=self):
            return
        self.session.submit(selected)
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        if self.session.advance():
            self._show_question()
        else:
            self._finish_quiz()

    def _finish_quiz(self) -> None:
        assert self.session is not None
        elapsed = max(0, int(__import__("time").monotonic() - self.quiz_started))
        summary = self.session.summary(elapsed)
        review = [{"question": a.question.prompt, "options": list(a.question.options),
                   "selected": a.selected, "answer": a.question.answer,
                   "explanation": a.question.explanation} for a in self.session.answers]
        self.result_id = self.database.save_result(self.player, self.category, self.difficulty, summary, review)
        self._show_result(self.database.get_result(self.result_id))

    def _show_result(self, result: dict) -> None:
        root = self._clear()
        self._header(root, "Quiz complete", f"{result['player_name']} · {result['category']} · {result['difficulty']}")
        card = ttk.Frame(root, style="Card.TFrame", padding=24)
        card.pack(fill="x", pady=8)
        ttk.Label(card, text=f"{result['percentage']:.0f}%", style="Card.TLabel",
                  font=("Segoe UI", 38, "bold")).pack(anchor="w")
        ttk.Label(card, text=performance_message(result["percentage"]), style="Card.TLabel",
                  font=("Segoe UI", 14)).pack(anchor="w", pady=(3, 18))
        rows = [("Questions", result["total"]), ("Correct", result["correct"]),
                ("Incorrect", result["incorrect"]), ("Unanswered", result["unanswered"]),
                ("Score", f"{result['score']} / {result['total']} points"),
                ("Time taken", self._format_duration(result["duration_seconds"]))]
        for label, value in rows:
            line = ttk.Frame(card, style="Card.TFrame")
            line.pack(fill="x", pady=4)
            ttk.Label(line, text=label, style="Card.TLabel").pack(side="left")
            ttk.Label(line, text=str(value), style="Card.TLabel", font=("Segoe UI", 11, "bold")).pack(side="right")
        actions = ttk.Frame(root)
        actions.pack(fill="x", pady=(18, 0))
        ttk.Button(actions, text="Review Answers", style="Accent.TButton", command=lambda: self.show_review(result)).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Restart Quiz", command=self._restart).pack(side="left", padx=8)
        ttk.Button(actions, text="Return to Home", command=self.show_home).pack(side="right")

    @staticmethod
    def _format_duration(seconds: int) -> str:
        return f"{seconds // 60}m {seconds % 60}s"

    def _restart(self) -> None:
        self.category = self.category
        self.show_home()
        self.category_var.set(self.category)
        self.difficulty_var.set(self.difficulty)
        self.name_var.set(self.player)
        self.start_quiz()

    def show_review(self, result: dict) -> None:
        root = self._clear()
        self._header(root, "Answer review", f"{result['player_name']} · {result['category']} · {result['difficulty']}")
        text = tk.Text(root, wrap="word", font=("Segoe UI", 11), bg=self.surface, fg=self.fg,
                       relief="flat", padx=18, pady=18, spacing1=5, spacing3=8)
        text.pack(fill="both", expand=True)
        text.tag_configure("correct", foreground="#15803d")
        text.tag_configure("wrong", foreground="#dc2626")
        text.tag_configure("heading", font=("Segoe UI", 12, "bold"))
        for i, item in enumerate(json.loads(result["review_json"]), 1):
            text.insert("end", f"{i}. {item['question']}\n", "heading")
            selected = item["selected"]
            if not selected:
                text.insert("end", "Your answer: Unanswered\n", "wrong")
            elif selected == item["answer"]:
                text.insert("end", f"Your answer: {selected} (Correct)\n", "correct")
            else:
                text.insert("end", f"Your answer: {selected} (Incorrect)\n", "wrong")
                text.insert("end", f"Correct answer: {item['answer']}\n", "correct")
            text.insert("end", f"Why: {item['explanation']}\n\n")
        text.configure(state="disabled")
        ttk.Button(root, text="Back to Results", command=lambda: self._show_result(result)).pack(anchor="e", pady=(12, 0))

    def show_history(self) -> None:
        root = self._clear()
        self._header(root, "Results history", "Your recent quiz attempts are saved on this device.")
        columns = ("date", "name", "category", "difficulty", "score", "percentage")
        tree = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")
        headings = {"date": "Date", "name": "Player", "category": "Category", "difficulty": "Level", "score": "Score", "percentage": "Result"}
        widths = {"date": 150, "name": 110, "category": 180, "difficulty": 80, "score": 75, "percentage": 80}
        for column in columns:
            tree.heading(column, text=headings[column])
            tree.column(column, width=widths[column], anchor="w")
        tree.pack(fill="both", expand=True)
        records = self.database.get_results()
        ids: dict[str, dict] = {}
        for record in records:
            iid = str(record["id"])
            ids[iid] = record
            tree.insert("", "end", iid=iid, values=(record["played_at"], record["player_name"], record["category"],
                        record["difficulty"], f"{record['score']}/{record['total']}", f"{record['percentage']:.0f}%"))
        actions = ttk.Frame(root)
        actions.pack(fill="x", pady=(14, 0))
        def review_selected() -> None:
            selection = tree.selection()
            if not selection:
                messagebox.showinfo("Select an attempt", "Choose a quiz attempt to review.", parent=self)
                return
            record = self.database.get_result(int(selection[0]))
            if record:
                self.show_review(record)
        ttk.Button(actions, text="Review Attempt", command=review_selected).pack(side="left")
        ttk.Button(actions, text="Clear History", command=self._clear_history).pack(side="left", padx=8)
        ttk.Button(actions, text="Return to Home", command=self.show_home).pack(side="right")
        if not records:
            ttk.Label(root, text="No quiz attempts yet. Complete a quiz and your results will appear here.", style="Muted.TLabel").pack(anchor="w", pady=10)

    def _clear_history(self) -> None:
        if messagebox.askyesno("Clear history?", "This permanently deletes all saved quiz results. Continue?", parent=self):
            self.database.clear_results()
            self.show_history()

    def show_settings(self) -> None:
        root = self._clear()
        self._header(root, "Settings", "Adjust the quiz experience. Changes are saved on this device.")
        card = ttk.Frame(root, style="Card.TFrame", padding=24)
        card.pack(fill="x")
        card.columnconfigure(1, weight=1)
        self.questions_var = tk.IntVar(value=self.settings["questions_per_quiz"])
        self.timer_var = tk.BooleanVar(value=self.settings["timer_enabled"])
        self.seconds_var = tk.IntVar(value=self.settings["timer_seconds"])
        self.dark_var = tk.BooleanVar(value=self.settings["dark_mode"])
        self.sound_var = tk.BooleanVar(value=self.settings["sound_enabled"])
        ttk.Label(card, text="Questions per quiz", style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=9)
        ttk.Spinbox(card, from_=1, to=20, textvariable=self.questions_var, width=8).grid(row=0, column=1, sticky="w", padx=15)
        ttk.Checkbutton(card, text="Enable countdown timer", variable=self.timer_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=9)
        ttk.Label(card, text="Seconds per question", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=9)
        ttk.Spinbox(card, from_=5, to=300, textvariable=self.seconds_var, width=8).grid(row=2, column=1, sticky="w", padx=15)
        ttk.Checkbutton(card, text="Dark mode", variable=self.dark_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=9)
        ttk.Checkbutton(card, text="Sound effects (not available in this build)", variable=self.sound_var, state="disabled").grid(row=4, column=0, columnspan=2, sticky="w", pady=9)
        actions = ttk.Frame(root)
        actions.pack(fill="x", pady=18)
        ttk.Button(actions, text="Save Settings", style="Accent.TButton", command=self._save_settings).pack(side="left")
        ttk.Button(actions, text="Reset to Defaults", command=self._reset_settings).pack(side="left", padx=8)
        ttk.Button(actions, text="Return to Home", command=self.show_home).pack(side="right")

    def _save_settings(self) -> None:
        try:
            questions = self.questions_var.get()
            seconds = self.seconds_var.get()
            if not 1 <= questions <= 20 or not 5 <= seconds <= 300:
                raise ValueError
        except (tk.TclError, ValueError):
            messagebox.showerror("Invalid settings", "Choose 1–20 questions and 5–300 seconds per question.", parent=self)
            return
        self.settings.update(questions_per_quiz=questions, timer_enabled=self.timer_var.get(),
                             timer_seconds=seconds, dark_mode=self.dark_var.get())
        self.database.save_settings(self.settings)
        self._apply_theme()
        self.show_home()

    def _reset_settings(self) -> None:
        self.settings = DEFAULT_SETTINGS.copy()
        self.database.save_settings(self.settings)
        self._apply_theme()
        self.show_settings()


if __name__ == "__main__":
    try:
        QuizApp().mainloop()
    except Exception as exc:
        messagebox.showerror("Python Quiz Master", f"The application could not start:\n{exc}")

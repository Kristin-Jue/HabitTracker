from habit_db import add_habit, increment_habit, delete_habit
from datetime import date


class HabitTracker:
    """
    HabitTracker class, enables to add a new habit, a new event, or delete a habit
    """

    def __init__(self, name: str, periodicity: int = None):
        self.name = name
        self.periodicity = periodicity

    def store(self, db):
        add_habit(db, self.name, self.periodicity)

    def add_event(self, db, event_date: date):
        increment_habit(db, self.name, event_date)

    def delete_habit(self, db):
        delete_habit(db, self.name)

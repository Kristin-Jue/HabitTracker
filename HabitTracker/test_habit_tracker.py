import datetime as dt

import analyse_habits
import habit_tracker
from habit_db import get_db, add_habit, increment_habit, get_habit_tracker


class TestHabitTracker:

    def setup_method(self):
        self.db = get_db("test1.db")
        add_habit(self.db, "test_habit", 1, dt.date(2022, 3, 1))
        add_habit(self.db, "test_habit_1", 1, dt.date(2022, 3, 1))
        add_habit(self.db, "test_habit_2", 1, dt.date(2022, 3, 1))
        add_habit(self.db, "test_habit_weekly", 7, dt.date(2022, 3, 1))
        add_habit(self.db, "test_habit_weekly_1", 7, dt.date(2022, 3, 1))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 13))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 14))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 15))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 16))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 18))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 20))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 21))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 23))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 24))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 27))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 28))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 29))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 30))
        increment_habit(self.db, "test_habit", dt.date(2022, 3, 31))
        increment_habit(self.db, "test_habit", dt.date(2022, 4, 1))
        increment_habit(self.db, "test_habit", dt.date(2022, 4, 2))
        increment_habit(self.db, "test_habit", dt.date(2022, 4, 3))
        increment_habit(self.db, "test_habit", dt.date(2022, 4, 4))
        increment_habit(self.db, "test_habit", dt.date(2022, 4, 5))
        increment_habit(self.db, "test_habit_1", dt.date(2022, 3, 20))
        increment_habit(self.db, "test_habit_1", dt.date(2022, 3, 21))
        increment_habit(self.db, "test_habit_1", dt.date(2022, 3, 22))
        increment_habit(self.db, "test_habit_1", dt.date(2022, 3, 23))
        increment_habit(self.db, "test_habit_1", dt.date(2022, 3, 25))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 13))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 14))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 15))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 16))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 17))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 18))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 19))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 20))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 21))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 5, 22))
        increment_habit(self.db, "test_habit_2", dt.date(2022, 6, 16))
        increment_habit(self.db, "test_habit_weekly", dt.date(2022, 2, 1))
        increment_habit(self.db, "test_habit_weekly", dt.date(2022, 2, 8))
        increment_habit(self.db, "test_habit_weekly", dt.date(2022, 2, 15))
        increment_habit(self.db, "test_habit_weekly", dt.date(2022, 2, 22))
        increment_habit(self.db, "test_habit_weekly", dt.date(2022, 3, 1))
        increment_habit(self.db, "test_habit_weekly_1", dt.date(2022, 3, 7))
        increment_habit(self.db, "test_habit_weekly_1", dt.date(2022, 3, 14))
        increment_habit(self.db, "test_habit_weekly_1", dt.date(2022, 3, 25))
        increment_habit(self.db, "test_habit_weekly_1", dt.date(2022, 3, 28))
        increment_habit(self.db, "test_habit_weekly_1", dt.date(2022, 4, 4))

    def test_db_habit_tracker(self):
        data = get_habit_tracker(self.db, dt.date(2022, 3, 1), "test_habit_1")
        assert len(data) == 5

    def test_db_habit_tracker_1(self):
        data1 = get_habit_tracker(self.db, dt.date(2022, 3, 21), "test_habit_1")
        assert len(data1) == 4

    def test_db_habit_tracker_2(self):
        data2 = analyse_habits.return_habit_names(self.db, 1)
        assert len(data2) == 3

    def test_db_habit_tracker_3(self):
        habit_tracker.delete_habit(self.db, 'test_habit_2')
        data3 = analyse_habits.return_habit_names(self.db, 1)
        assert len(data3) == 2

    def test_db_habit_tracker_4(self):
        data3 = analyse_habits.return_habit_names(self.db, 7)
        assert len(data3) == 2

    def test_db_habit_tracker_5(self):
        data4 = analyse_habits.return_number_of_habit_streaks(self.db, name='test_habit')
        assert data4 == ('test_habit', 10)

    def test_db_habit_tracker_6(self):
        data5 = analyse_habits.return_number_of_habit_streaks(self.db, periodicity=1)
        assert data5 == (['test_habit', 'test_habit_2'], 10)

    def test_db_habit_tracker_7(self):
        data6 = analyse_habits.return_number_of_habit_streaks(self.db, periodicity=7)
        assert data6 == (['test_habit_weekly', 'test_habit_weekly_1'], 5)

    def test_db_habit_tracker_8(self):
        """
        This is difficult to test, as all resets will be counted and it will check until today's date. On 2022-06-24 it
        was 32 resets, but of course if you test this later, this number has to be incremented
        """

    # data7 = analyse_habits.return_number_of_habit_resets(self.db, name='test_habit_2')
    # assert data7 == ('test_habit_2', 32)

    def teardown_method(self):
        import os
        os.remove("test1.db")

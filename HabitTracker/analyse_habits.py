import datetime as dt
from pandas import date_range
from habit_db import get_habit_names, get_habit_tracker, get_periodicity, get_first_check_off_date


def return_habit_names(db, periodicity: int = None):
    """
    returns a list of defined habits, if wanted only for a certain periodicity

    :param db: database where the data is stored
    :param periodicity: if periodicity is specified, only habits with this periodicity will be returned, otherwise all
    predefined habits will be returned
    :return: list with habits
    """
    data = get_habit_names(db, periodicity)
    return data


def get_habit_streak(db, name: str, time_interval: float = None):
    """
    returns a dictionary with all dates where a habit was supposed to be checked off and a Boolean value whether the
    habit was checked-off on that date

    :param db: database where the data is stored
    :param name: habit for which the check-off data is extracted
    :param time_interval: if a time interval is provided, only data for a certain amount of time is extracted,
                      otherwise all data is extracted
    :return: dictionary, key = date, value= True when habit was completed on this day, False if it was not completed
    """
    periodicity = int(get_periodicity(db, name))
    if not time_interval:
        start_date = dt.date(2000, 1, 1)
    else:
        start_date = dt.date.today() - dt.timedelta(days=time_interval)

    data = get_habit_tracker(db, start_date, name)

    if not data:

        """
          if data is empty, it is possible that either this habit has never been checked off, or that it just has not been
          checked off in the specified time period and therefore missed to check it off during this time. If it has never 
          been checked off an empty dictionary is returned, otherwise a dictionary with False as the value for each day 
          where it was supposed to be checked off
          """

        first_date = get_first_check_off_date(db, name)
        if first_date is None:
            return dict()
        else:
            date_list_check = dict()
            for i in range(time_interval):
                date_list_check[i] = False
            return date_list_check

    else:
        # data is split into a list with the habit name and a list when that habit was checked off
        names_list, dates_list = zip(*data)

        first_date = get_first_check_off_date(db, name)
        if first_date == min(dates_list):
            list_start_date = dt.datetime.strptime(min(dates_list), '%Y-%m-%d').date()
        else:
            list_start_date = start_date

        delta = dt.date.today() - list_start_date
        date_list_check = dict()

        day = list_start_date

        # goes through the dates when the habit was supposed to be checked off, if it was checked of sets dictionary
        # value for that fay as true, otherwise as False

        for day_iterator in range(int((delta.days + periodicity) / periodicity)):
            # date_range returns all possible dates within a certain timeframe, mostly important when periodicity ==7,
            # as the task can be completed on multiple days within this 7 days period.

            dates_range_list = date_range(day, day + dt.timedelta(days=periodicity - 1))
            day_string = day.strftime('%Y-%m-%d')
            dates_set_string = set(dates_range_list.strftime('%Y-%m-%d'))

            # checks whether the check-off date has an overlap with the allowed check off dates
            if not dates_set_string.isdisjoint(set(dates_list)):
                date_list_check[day_string] = True
            else:
                date_list_check[day_string] = False
            day = day + dt.timedelta(days=periodicity)

        return date_list_check


def get_habit_streak_for_all_habits(db, timeframe: float = None, periodicity: int = None):
    """
    returns a nested dictionary which includes a dictionary with all dates where a habit was supposed to be checked off
    and a Boolean value whether the habit was checked-off on that date for each habit

    :param db: database where the data is stored
    :param timeframe: if a timeframe is provided, only data for a certain amount of time is extracted,
    otherwise all data is extracted
    :param periodicity: if periodicity is proved, only habits with this periodicity will be analysed
    :return: nested dictionary
    """
    habit_name_list = get_habit_names(db, periodicity)
    habits_streak_list = dict()
    for habit_name in habit_name_list:
        habits_streak_list[habit_name] = get_habit_streak(db, habit_name, timeframe)
    return habits_streak_list


def return_number_of_habit_streaks(db, name: str = None, time_interval: float = None, periodicity: int = None):
    """
    returns the maximum habit streak for one habit if provided or checks the largest streak over all habits

    :param db: database where the data is stored
    :param name:
    :param time_interval: if a timeframe is provided, only data for a certain amount of time is extracted,
    otherwise all data is extracted
    :param periodicity: if periodicity is proved, only habits with this periodicity will be analysed
    :return: name and maximum habit streak
    """
    if not name:
        """
        if no name is provided, all habits will be checked for their longest streak and the longest overall streak will 
        be returned 
        """
        data = get_habit_streak_for_all_habits(db, time_interval, periodicity)
        longest_streak_dict = dict()

        for habit_name, habit_tracker in data.items():
            streak = 0
            longest_streak = 0

            for key, value in habit_tracker.items():
                if value:
                    streak += 1
                    if streak > longest_streak:
                        longest_streak = streak
                else:
                    streak = 0

            longest_streak_dict[habit_name] = longest_streak

        max_longest_streak = max(longest_streak_dict.values())
        # checks whether there are multiple habits with the longest habit streak
        longest_streak_name = [key for key, value in longest_streak_dict.items() if value == max_longest_streak]

        return longest_streak_name, max_longest_streak

    else:

        """
        if a specific habit is provided only this habit will be checked for the longest check off streak
        """
        data = get_habit_streak(db, name, time_interval)

        streak = 0
        longest_streak = 0

        for key, value in data.items():
            if value:
                streak += 1
            else:
                if streak > longest_streak:
                    longest_streak = streak
                streak = 0

        return name, longest_streak


def return_number_of_habit_resets(db, name: str = None, time_interval: float = None, periodicity: int = None):
    """
    returns the amount of habit resets for one habit if provided or checks the largest reset number over all habits

    :param db: database where the data is stored
    :param name: if supplied, habit reset count will only be returned for this habit, otherwise all habits will be
    checked for the maximal reset count
    :param time_interval: if a timeframe is provided, only data for a certain amount of time is extracted,
    otherwise all data is extracted
    :param periodicity: if periodicity is proved, only habits with this periodicity will be analysed
    :return: name and count of habit resets
    """

    if not name:
        # if no name is provided, data for all habits will be extracted
        data = get_habit_streak_for_all_habits(db, time_interval, periodicity)

        # initialise dictionary to store reset count for the individual habits
        reset_count_dict = dict()

        # loop to go through all different habits
        for name, date_check in data.items():
            reset_count = 0

            # loops through check-off dates
            for key, value in date_check.items():
                # if value == False, habit was not completed on this day, so reset count will be incremented
                if not value:
                    reset_count += 1
            reset_count_dict[name] = reset_count

        # check for highest reset count
        max_reset_count = max(reset_count_dict.values())
        # grabs all habit names that were reset most often (max_rest_count)
        max_reset_name = [key for key, value in reset_count_dict.items() if value == max_reset_count]

        return max_reset_name, max_reset_count

    # checks resets for a specified habit
    else:
        data = get_habit_streak(db, name, time_interval)
        reset_count = 0

        for key, value in data.items():
            if not value:
                reset_count += 1
        # returns habit name and its reset count
        return name, reset_count

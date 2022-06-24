import sqlite3
import datetime as dt
from sqlite3 import Connection


def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db: Connection):
    """
    creates a table to store the habits and a table to store the check-off dates if they do not already exist

    :param db: database where habit tracker data is stored
    :return: None
    """
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
        name TEXT PRIMARY KEY,
        periodicity INT,
        creation_date DATE)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habits_tracker (
        habitsName TEXT,
        check_off_date DATE,
        FOREIGN KEY (habitsName) REFERENCES habits(name))""")

    db.commit()


def add_habit(db: Connection, name: str, periodicity: int, creation_date: dt.date = None):
    """
    stores a new habit in a database

    :param db: database to store the habit
    :param name: habit name
    :param periodicity:habit periodicity
    :param creation_date: habit creation date, if not provided today's date will be stored
    :return: None
    """
    cur = db.cursor()
    if not creation_date:
        creation_date = dt.date.today()

    cur.execute("INSERT INTO habits VALUES (?, ?, ?)", (name, periodicity, creation_date))
    db.commit()


def increment_habit(db: Connection, name: str, event_date: dt.date):
    """
    stores a new check-off date for a defined habit

    :param db: database where habits are stored
    :param name: habit name for which the date will be stored
    :param event_date: date when the habit was completed
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habits_tracker VALUES (?, ?)", (name, event_date))
    db.commit()


def delete_habit(db: Connection, name: str):
    """
    deletes a habit

    :param db: database where habits are stored
    :param name: habit to be deleted
    :return: None
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE name =?", (name,))
    cur.execute("DELETE FROM habits_tracker WHERE habitsName = ?", (name,))
    db.commit()


def get_habit_names(db: Connection, periodicity: int = None):
    """
    returns a list with defined habits, if periodicity is supplied, only habits with this periodicity will be returned

    :param db: database where habits are stored
    :param periodicity: if provided, only habits with this periodicity will be returned
    :return: list with habit names
    """
    cur = db.cursor()
    if not periodicity:
        cur.execute("SELECT name FROM habits")
    else:
        cur.execute("SELECT name FROM habits WHERE periodicity=?", (periodicity,))
    return [x[0] for x in cur.fetchall()]


def get_periodicity(db: Connection, name: str):
    """
    return the periodicity for a certain habit

    :param db: database where habits are stored
    :param name: habit name for the wanted periodicity
    :return: periodicity
    """
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habits WHERE name=?", (name,))
    return cur.fetchone()[0]


def get_habit_tracker(db: Connection, start_date: dt.date, name: str = None):
    """
    Returns a tuple with habits and check off dates for a defined period of time. If a name is supplied, only data for
    this habit will be returned

    :param db: database where habits are stored
    :param start_date: earliest date for which data will be returned
    :param name: if supplied, only data for this habit will be returned
    :return: tuple with habits and check off dates
    """
    date_today = dt.date.today()
    cur = db.cursor()
    if not name:
        cur.execute("SELECT * FROM habits_tracker WHERE check_off_date BETWEEN ? AND ?",
                    (start_date, date_today,))
    else:
        cur.execute("SELECT * FROM habits_tracker WHERE habitsName=? AND check_off_date BETWEEN ? AND ?",
                    (name, start_date, date_today,))
    return cur.fetchall()


def get_first_check_off_date(db: Connection, name: str):
    """
    Returns the first check-off date for a specified habit

    :param db:database where habits are stored
    :param name: name for the table for which the first check off date should be returned
    :return: first check off date
    """

    cur = db.cursor()
    cur.execute('SELECT MIN(check_off_date) FROM habits_tracker WHERE habitsName=?', (name,))
    return cur.fetchone()[0]

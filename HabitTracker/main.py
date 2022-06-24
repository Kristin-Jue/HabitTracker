import PyInquirer as pyi
from analyse_habits import return_habit_names, return_number_of_habit_streaks, return_number_of_habit_resets
from habit_tracker import HabitTracker
from habit_db import get_db
from prompt_toolkit.validation import Validator, ValidationError
import datetime as dt


class DateValidator(Validator):
    """
    checks whether an entered date is a valid date, if not throws an exception and tells the user to enter a valid date
    """
    def validate(self, document):
        try:
            dt.datetime.strptime(str(document.text), '%Y-%m-%d')
        except ValueError:
            raise ValidationError(
                message='Please enter a valid date',
                cursor_position=len(document.text))  # Move cursor to end


def user_options():
    """
    Asks the user what they want to do
    :return: user answer
    """
    user_prompt = {
        'type': 'list',
        'name': 'input',
        'message': 'What do you want to do?',
        'choices': [
            'Add a new habit',
            'Check off a habit',
            'Delete a habit',
            'Analyse my habits',
            'Exit'
        ]
    }
    answers = pyi.prompt(user_prompt)
    return answers['input']


def list_of_habits(answers=None):
    """
    returns a list of habits that already exist in the database and adds the options  'exit', if answers is set to True,
     the option 'For all habits' will be added

    :return: list of options
    """
    habit_names = return_habit_names(db)
    habit_names.append('Exit')
    if answers:
        habit_names.insert(0, 'For all habits')
    return habit_names


def new_habit_input():
    """
    Asks the user to enter a new habit name and then in what periodicity they want to check it off, every day, or once a
    week

    :return: user answer
    """
    user_prompt = [
        {
            'type': 'input',
            'name': 'new_habit_name',
            'message': 'What\'s the name of your new habit?',
        },
        {
            'type': 'list',
            'name': 'new_habit_periodicity',
            'message': 'How often would you like to perform this habit?',
            'choices': ['Every day', 'Once a week']

        }
    ]
    answers = pyi.prompt(user_prompt)
    return answers


def check_off_habit_input():
    """
    Presents the user with their list of habits and asks them which of those they want to check-off, they can then
    decide whether they want to check it off late (i.e. for a previous date). If yes, they need to enter this date.

    :return: user answer
    """
    user_prompt = [
        {
            'type': 'list',
            'name': 'input',
            'message': 'Which habit would you like to check off?',
            'choices': list_of_habits(),
        },
        {
            'type': 'confirm',
            'message': 'Do you want to check-off this habit late?',
            'name': 'confirmation',
            'default': False,
            'when': lambda answers: answers['input'] != 'Exit',
        },
        {
            'type': 'input',
            'name': 'check_off_date',
            'message': 'When did you complete this habit? (Please enter a date in the form YYYY-MM-DD)',
            'when': lambda answers: answers['input'] != 'Exit' and answers['confirmation'],
            'validate': DateValidator
        }
    ]
    answers = pyi.prompt(user_prompt)
    if answers['input'] == 'Exit':
        main()
    else:
        return answers


def delete_habit_input():
    """
    Presents the user with their list of habits and lets them chose which one of those they want to delete. Then the
    user as to confirm that they really want to delete that habit.

    :return: user answer
    """
    user_prompt = [
        {
            'type': 'list',
            'name': 'input',
            'message': 'Which habit would you like to delete?',
            'choices': list_of_habits(),
        },
        {
            'type': 'confirm',
            'message': 'Are you sure you want to delete this habit?',
            'name': 'confirmation',
            'default': False,
            'when': lambda answers: answers['input'] != 'Exit',
        }

    ]
    answers = pyi.prompt(user_prompt)
    if answers['input'] == 'Exit':
        main()
    else:
        return answers


def analyse_habit_input():
    """
    asks the user what the want to analyse about their habits

    :return: user input
    """
    user_prompt = {
        'type': 'list',
        'name': 'input',
        'message': 'What do you want to know?',
        'choices': [
            'What’s my longest habit streak?',
            'What\'s the list of my current daily habits?',
            'What\'s the list of my current weekly habits?',
            'With which habit did I struggle most with last month?',
            'Exit'
        ]
    }
    answers = pyi.prompt(user_prompt)
    return answers['input']


def choice_habit_to_analyse():
    """
    presents a list of habits that can be analysed

    :return: user input
    """
    user_prompt = {
        'type': 'list',
        'name': 'input',
        'message': 'For which habit would you like to know?',
        'choices': list_of_habits(True)
    }
    answers = pyi.prompt(user_prompt)
    return answers['input']


def ask_to_continue():
    """
    Asks the user whether they want to do perform any other action or not.
    :return: user input
    """
    user_prompt = {
        'type': 'confirm',
        'message': 'Do you want to perform any other action?',
        'name': 'confirmation',
        'default': True,
    }
    answers = pyi.prompt(user_prompt)
    if answers['confirmation']:
        main()
    else:
        print('Alright! See you next time.')


def main():
    user_input = user_options()
    if user_input == 'Add a new habit':
        data = new_habit_input()
        name = data['new_habit_name']
        periodicity = 0
        if data['new_habit_periodicity'] == 'Every day':
            periodicity = 1
        elif data['new_habit_periodicity'] == 'Once a week':
            periodicity = 7
        tracker = HabitTracker(name, periodicity)
        tracker.store(db)
        ask_to_continue()
    elif user_input == 'Check off a habit':
        data = check_off_habit_input()
        try:
            name = data['input']
        except TypeError:
            pass
        else:
            if data['confirmation']:
                check_off_date = data['check_off_date']
            else:
                check_off_date = dt.date.today().strftime("%Y-%m-%d")
            tracker = HabitTracker(name)
            tracker.add_event(db, check_off_date)
            ask_to_continue()
    elif user_input == 'Delete a habit':
        answer = delete_habit_input()
        if answer['input'] == 'Exit':
            main()
        else:
            habit_to_be_deleted = answer['input']
            if answer['confirmation']:
                tracker = HabitTracker(habit_to_be_deleted)
                tracker.delete_habit(db)
                print(f'The habit: "{habit_to_be_deleted}" has been deleted successfully ')
                ask_to_continue()
            elif not answer['confirmation']:
                print(f'Ok,"{habit_to_be_deleted}" will not be deleted, you will be redirected to the main menu')
                main()
    elif user_input == 'Analyse my habits':
        analyse = analyse_habit_input()
        if analyse == 'What’s my longest habit streak?':
            choice = choice_habit_to_analyse()
            if choice == 'For all habits':
                data = return_number_of_habit_streaks(db)
                names = list(data[0])
                print(f"The longest habit streak for your habit(s) '{' and '.join([str(x) for x in [*names]])}' "
                      f"was: ", data[1])

            elif choice == 'Exit':
                main()
            else:
                number = return_number_of_habit_streaks(db, choice)
                print(f'The longest habit streak for your habit "{choice}" was: ', number[1])
        if analyse == 'What\'s the list of my current daily habits?':
            print('Your current daily habits are:', *return_habit_names(db, 1), sep="\n")
        if analyse == 'What\'s the list of my current weekly habits?':
            print('Your current weekly habits are:', *return_habit_names(db, 7), sep="\n")
        if analyse == 'With which habit did I struggle most with last month?':
            data = return_number_of_habit_resets(db, time_interval=30)
            names = list(data[0])
            print(f"During the last month you struggled most with your habit(s) "
                  f"'{' and '.join([str(x) for x in [*names]])}', you missed it {data[1]} times")
        ask_to_continue()
    else:
        print('Goodbye! See you next time')


if __name__ == '__main__':
    db = get_db()
    print("Welcome to your HabitTracker App!")
    main()

# My HabitTracker Project

This is a command line interface with which you can define habits and track your progress in completing them. 


## Usage

1. Define habits you want to complete regularly
2. Decide how often you want to complete them: Every day or once a week
3. Analyse your habits and see how successful you were in your endeavors

## Installation

Open a terminal in a folder of your choosing where you want the HabitTracker to be located. Afterwards just copy the 
following commands into your command line.

Attention, Python3 needs to be installed on your computer to use this app. If you don't have it installed already, 
go to https://www.python.org/downloads/ and follow the instructions on the website. Afterwards continue as explained 
above. 

```
git clone https://github.com/Kristin-Jue/HabitTracker
cd HabitTracker/HabitTracker
pip install -r requirements.txt
```


## How to start the app

To start the interface, just start the interface with the following command

```
python main.py
```

## Tests 

To test the usage of the app, you can use pytest.

```
pytest .
```

Further a sample database 'main.db' is already supplied. \
If you don't want this, just delete the file from your directory.

# My HabitTracker Project

This is a command line interface with which you can define habits and track your progress in completing them. 


## Usage

1. Define habits you want to complete regularly
2. Decide how often you want to complete them: Every day or once a week
3. Analyse your habits and see how successful you were in your endeavors

Note: To successfully check off your weekly habits you always have the whole week to check them off

## Installation

Open a terminal in a folder of your choosing where you want the HabitTracker to be located. Afterwards just copy the 
following commands into your command line.


```
git clone https://github.com/Kristin-Jue/HabitTracker
cd HabitTracker/HabitTracker
pip3 install -r requirements.txt
```
Attention, Python3 needs to be installed on your computer to use this interface. If you don't have it installed already, 
go to https://www.python.org/downloads/ and follow the instructions on the website. Afterwards continue as explained 
above. 

## How to start the app

To start the interface, just type in the following command 

```
python3 main.py
```

## Tests 

To test the usage of the app, you can use pytest. 

```
pytest .
```

Further, a sample database with 5 predefined habits ('main.db') is already supplied. \
If you don't want this, just delete the file from your directory and start defining your own habits! .

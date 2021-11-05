#!/usr/bin/env python3

import streamlit as st
from ics import Calendar, Event
import yaml
import sys, getopt
import datetime
from calendar import monthrange


class classes:
    def __init__(self, name, classroom, teacher):
        self.name = name
        self.classroom = classroom
        self.teacher = teacher


st.title('Ibbycal')

st.subheader('Configuration')

# Uploading and parsing config
inputFile = st.file_uploader("Upload yaml config", type=['yaml', 'yml'])

if inputFile is not None:
    data = yaml.safe_load(inputFile)
else:
    st.stop()

# Creating a dictionary of classes from config.yaml
dictofclass = {}
for i in data['classes']:
    dictofclass.update({i['name']: classes(i['name'], i['classroom'], i['teacher'])})

# Create an array for timetable
timetable = list()
for i in data['timetable']:
    timetable.append(i)

# Create an array for weekend
weekend = list()
for i in data['weekend']:
    weekend.append(i)


st.subheader("Generate")

date = st.date_input("Current Day")
cycle = st.slider("Current Cycle", 1, len(timetable))
cycle -= 1
duration = st.number_input("How many days to generate to?", 1) 

if st.checkbox("No day?"):
    noDay = True
else: 
    noDay = False

year, month, date = str(date).split('-')

year = int(year)
month = int(month)
date = int(date)

# Begin is an arrow object
classTimes = ["08:25:00", "10:00:00", "11:25:00", "14:05:00"]
# May be set to anything that timedelta() understands/May be set with a dict
classDuration = {"hours": 1, "minutes": 20}

c = Calendar()
week = list()
cyclecount = len(timetable)

currentDay = date
currentMonth = month
currentYear = year
for dayCount in range(duration):
    # Checking if next month
    if currentDay > monthrange(currentDay, currentMonth)[1]:
        currentDay = currentDay % monthrange(currentYear, currentMonth)[1]
        currentMonth += 1
        
    # Checking if next year
    if currentMonth > 12:
        currentMonth = currentMonth % 12
        currentYear += 1

    # Checking if weekend
    while datetime.date(year=currentYear, month=currentMonth, day=currentDay).strftime("%A") in weekend:
        currentDay += 1

        # Checking if next month
        if currentDay > monthrange(currentDay, currentMonth)[1]:
            currentDay = currentDay % monthrange(currentYear, currentMonth)[1]
            currentMonth += 1

        # Checking if next year
        if currentMonth > 12:
            currentMonth = currentMonth % 12
            currentYear += 1

    day = list()
    currentCycle = (dayCount+cycle)%cyclecount
    for j in range(len(timetable[currentCycle])):
        # skip class if free session
        if timetable[currentCycle][j] in ("free", "Free"):
            continue

        day.append(Event(name=dictofclass[timetable[currentCycle][j]].name,
                         begin=f"{currentYear:04}-{currentMonth:02}-{currentDay:02} {classTimes[j]}+08:00",
                         duration=classDuration,
                         location=dictofclass[timetable[currentCycle][j]].classroom))

    # Create all day event showing Day Number
    if noDay is not True:
        foo = Event(name="Day "+str(currentCycle+1), begin=f"{currentYear:04}-{currentMonth:02}-{currentDay:02}")
        foo.make_all_day()
        day.append(foo)

    currentDay += 1
    week.append(day)

# Adding calendar objects for each day
for i in range(len(week)):
    for j in week[i]:
        c.events.add(j)

# Output file
st.subheader("Download your file!")
st.download_button("Download file", str(c), "timetables.ics", "text/Calendar")

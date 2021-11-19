#!/usr/bin/env python3

import streamlit as st
from ics import Calendar, Event
from io import StringIO
import yaml
import datetime
import pytz


class classes:
    def __init__(self, name, classroom, teacher):
        self.name = name
        self.classroom = classroom
        self.teacher = teacher


st.title('Ibbycal')

st.sidebar.subheader('Configuration')

# Uploading and parsing config
inputFile = st.sidebar.file_uploader("Upload yaml config", type=['yaml', 'yml'], help="Upload your generated configuration file here")

if inputFile is not None:
    try:
        data = yaml.safe_load(inputFile)

    except yaml.YAMLError as exc:
        if hasattr(exc, 'problem_mark'):
            if exc.context != None:
                st.error('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                    str(exc.problem) + ' ' + str(exc.context) +
                    '\nPlease correct data and retry.')
                st.stop()
            else:
                st.error('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                    str(exc.problem) + '\nPlease correct data and retry.')
                st.stop()
        else:
            st.error("Something went wrong while parsing yaml file")
            st.stop()
else:
    st.warning("Upload configuration file from sidebar")
    st.stop()

# Holiday file
holiday = False
if st.sidebar.checkbox("holiday config", help="Upload an ics containing holiday events"):
    inputFile = st.sidebar.file_uploader("Upload holiday config", type=['ics'])

    if inputFile is not None:
        c = Calendar(StringIO(inputFile.getvalue().decode("utf-8")).read())
        holiday = True

        e = list(c.timeline)
        holidayDates = list()
        for i in e:
            holidayDates.append(i.begin.date())

# Creating a dictionary of classes from config.yaml
dictofclass = {}
try:
    for i in data['classes']:
        dictofclass.update({i['name']: classes(i['name'], i['classroom'], i['teacher'])})
except KeyError:
    st.error("Classes section in configuration is broken")
    st.stop()

if len(dictofclass) <= 0:
    st.error("Configuration file error: check classes")
    st.stop()

# Create an array for timetable
timetable = list()

try:
    for i in data['timetable']:
        timetable.append(i)
except KeyError:
    st.error("Timetable section in configuration is broken")
    st.stop()

# Create an array for weekend
weekend = list()
try:
    for i in data['weekend']:
        weekend.append(i)
except KeyError:
    st.error("Weekend section in configuration is broken")
    st.stop()

date = st.date_input("Current Day", help="Enter the day you want to start generating timetables for")
cycle = st.slider("Current Cycle", 1, len(timetable), help="Enter the cycle of the day selected")
cycle -= 1
duration = st.number_input("How many days generate?", 1)

if st.checkbox("No day", help="If enabled, the calendar will not generate all day events showing the cycle"):
    noDay = True
else: 
    noDay = False

classTimes = list()
tz = pytz.timezone('Asia/Shanghai')
for i in ["08:25:00", "10:00:00", "11:25:00", "14:05:00"]:
    classTimes.append(datetime.datetime.strptime(i, '%H:%M:%S').time().replace(tzinfo=tz))
classDuration = {"hours": 1, "minutes": 20}

c = Calendar()
week = list()
cyclecount = len(timetable)

if cyclecount <= 0:
    st.error("Configuration file error: check timetable")
    st.stop()

currentDay = date
for dayCount in range(duration):
    # Checking if weekend
    while currentDay.strftime("%A") in weekend:
        currentDay += datetime.timedelta(days=1)

    # Checking if holiday
    if holiday is True:
        while currentDay in holidayDates:
            currentDay += datetime.timedelta(days=1)

    day = list()
    currentCycle = (dayCount+cycle)%cyclecount
    for j in range(len(timetable[currentCycle])):
        # skip class if free session
        if timetable[currentCycle][j] in ("free", "Free"):
            continue

        day.append(Event(name=dictofclass[timetable[currentCycle][j]].name,
                         begin=datetime.datetime.combine(currentDay, classTimes[j]),
                         duration=classDuration,
                         location=dictofclass[timetable[currentCycle][j]].classroom))

    # Create all day event showing Day Number
    if noDay is not True:
        foo = Event(name="Day "+str(currentCycle+1), begin=currentDay)
        foo.make_all_day()
        day.append(foo)

    currentDay += datetime.timedelta(days=1)
    week.append(day)

# Adding calendar objects for each day
for i in range(len(week)):
    for j in week[i]:
        c.events.add(j)

# Output file
st.subheader("Download your file!")
st.download_button("Generate!", str(c), "timetables.ics", "text/Calendar")

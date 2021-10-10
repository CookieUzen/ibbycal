#!/usr/bin/env python3

from ics import Calendar, Event
import yaml


class classes:
    def __init__(self, name, classroom, teacher):
        self.name = name
        self.classroom = classroom
        self.teacher = teacher


with open('config.yaml') as foo:
    data = yaml.safe_load(foo)

# Creating a dictionary of classes from config.yaml
dictofclass = {}
for i in range(len(data['classes'])):
    dictofclass.update({data['classes'][i]['name']:
                        classes(data['classes'][i]['name'],
                        data['classes'][i]['classroom'],
                        data['classes'][i]['teacher'])})

# Create an array for timetable
timetable = list()

for i in range(len(data['timetable'])):
    timetable.append(data['timetable'][i])

# Begin is an arrow object
classTimes = ["08:25:00", "10:00:00", "11:25:00", "14:05:00"]
# May be set to anything that timedelta() understands/May be set with a dict
classDuration = {"hours": 1, "minutes": 20}

c = Calendar()
day = []

for i in range(len(timetable[0])):
    day.append(Event(name=dictofclass[timetable[0][i]].name,
                     begin='2021-09-23 '+classTimes[i],
                     duration=classDuration,
                     location=dictofclass[timetable[0][i]].classroom))

for i in range(len(day)):
    c.events.add(day[i])

with open('my.ics', 'w') as my_file:
    my_file.writelines(c)

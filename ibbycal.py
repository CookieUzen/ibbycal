#!/usr/bin/env python3

from ics import Calendar, Event

# Begin is an arrow object
classTimes = ["08:25:00", "10:00:00", "11:25:00", "14:05:00"]
# May be set to anything that timedelta() understands/May be set with a dict
classDuration = {"hours": 1, "minutes": 20}


class Class:
    name = ""
    room = ""

    def __init__(self, name, room):
        """Constructor"""
        self.name = name
        self.room = room


mathClass = Class("math", "yeeeeet")

c = Calendar()
day = []

day.append(Event(name=mathClass.name, begin='2021-09-23 '+classTimes[2], duration=classDuration, location=mathClass.room))

for i in range(len(day)):
    c.events.add(day[i])

with open('my.ics', 'w') as my_file:
    my_file.writelines(c)

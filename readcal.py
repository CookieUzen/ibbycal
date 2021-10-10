#!/usr/bin/env python3

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

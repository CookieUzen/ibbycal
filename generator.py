#!/usr/bin/env python3

import yaml

# print("When are your workdays? [1 2 3-7]")

def addClass():
    """add classess"""
    classes = list()
    while True:
        print("Enter class name: ", end="")
        className = input()

        print("Enter classroom: ", end="")
        classRoom = input()

        print("Enter teacher: ", end="")
        classTeacher = input()

        classes.append({'name': className, 'classroom': classRoom, 'teacher': classTeacher})

        print("Add another class [Y/n]: ", end="")
        if input() in ('n', 'N', 'No', 'no'):
            break
        print()

    print()
    return(classes)


def addTimetable():
    """add timetable"""
    timetable = list()

    print("Input classes, with a comma seperating each class. Class name have to the ones entered above.")
    while True:
        read = input().split(",")
        strippedRead = [ i.strip() for i in read ]

        timetable.append(strippedRead)
        print("Add another day [Y/n]: ", end="")
        if input() in ('n', 'N', 'No', 'no'):
            break
        print()

    print()
    return(timetable)


output = {'classes': addClass(), 'timetable': addTimetable()}

with open('config.yaml', 'w') as file:
    yaml.dump(output, file)

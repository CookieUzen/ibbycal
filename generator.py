#!/usr/bin/env python3

import yaml

# print("When are your workdays? [1 2 3-7]")
# A = input()
# Parse this

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

        classes.append({'name': className, 'room': classRoom, 'teacher': classTeacher})

        print("Add another class [Y/n]: ", end="")
        if input() in ('n', 'N', 'No', 'no'):
            break

    print()
    return(classes)


def addTimetable():
    """add timetable"""
    timetable = list()
    while True:
        print("Input classes, with a space seperating each class. Class name have to the ones entered above.")
        timetable.append(input().split())

        print("Add another day [Y/n]: ", end="")
        if input() in ('n', 'N', 'No', 'no'):
            break

    print()
    return(timetable)


output = {'classes': addClass(), 'timetable': addTimetable()}

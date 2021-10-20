#!/usr/bin/env python3

import yaml

# print("When are your workdays? [1 2 3-7]")

def addClass():
    """add classess"""
    classes = list()
    print("Adding classes to database")
    while True:
        print("Enter class name: ", end="")
        className = input()
        if className == "":
            print("Cannot input empty classname, try again.\n")
            continue

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

    print("Adding the classes for each day")
    print("Use a comma seperating each class. Class name have to the ones entered above.")
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

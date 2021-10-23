#!/usr/bin/env python3

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


def usage():
    print("""Usage: ibbycal [OPTION]
               -h, --help       show help
               -c, --cycle      cycle for first day this week
               -y, --year       year of first day this week
               -m, --month      month of first day this week
               -d, --day        day of first day this week
               -a, --duration   how many days to generate
               """)


def main(argv):
    # Parsing arguements
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:y:m:d:a:", ["help", "cycle=", "year=", "month=", "day=", "duration="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        usage()
        sys.exit(2)

    for opts, args in opts:
        if opts in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opts in ("-c", "--cycle"):
            cycle = int(args)
        elif opts in ("-y", "--year"):
            year = int(args)
        elif opts in ("-m", "--month"):
            month = int(args)
        elif opts in ("-d", "--day"):
            date = int(args)
        elif opts in ("-a", "--duration"):
            duration = int(args)

    # Reading config file
    try:
        with open('config.yaml') as foo:
            data = yaml.safe_load(foo)
    except FileNotFoundError as err:
        print(err)
        print("config not found, exiting")

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
    
    # Sanity checking
    try:
        cycle
    except NameError:
        print("What's the cycle?: ", end="")
        cycle = int()
        while True:
            cycle = input()

            if cycle == "":
                print("Empty value, try again: ", end="")
                continue

            if int(cycle) > len(timetable):
                print("cycle is bigger than timetable, try again: ", end="")
                continue

            break

        cycle = int(cycle)

    try:
        year
    except NameError:
        print("year (press return for this year): ", end="")
        if (read := input()) == "":
            year = datetime.datetime.now().strftime("%Y")
        else:
            year = int(read)

    try:
        month
    except NameError:
        print("month (press return for this month): ", end="")
        if (read := input()) == "":
            month = datetime.datetime.now().strftime("%m")
        else:
            month = int(read)

    try:
        date
    except NameError:
        print("day (press return for today): ", end="")
        if (read := input()) == "":
            date = datetime.datetime.now().strftime("%d")
        else:
            date = int(read)

    try:
        duration
    except NameError:
        print("duration (press return for one day): ", end="")
        if (read := input()) == "":
            duration = 1
        else:
            duration = int(read)

    # recenter cycle so it matches array
    cycle = cycle - 1

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
        # Checking if next year
        if currentMonth >= 12:
            currentMonth = currentMonth % 12 + 1
            currentYear += 1

        # Checking if next month
        if currentDay >= monthrange(currentDay, currentMonth)[1]:
            currentDay = currentDay % monthrange(currentYear, currentMonth)[1] + 1
            currentMonth += 1
            
        # Checking if weekend
        while datetime.date(year=currentYear, month=currentMonth, day=currentDay).strftime("%A") in weekend:
            currentDay += 1

            # Checking if next year
            if currentMonth >= 12:
                currentMonth = currentMonth % 12 + 1
                currentYear += 1

            # Checking if next month
            if currentDay >= monthrange(currentDay, currentMonth)[1]:
                currentDay = currentDay % monthrange(currentYear, currentMonth)[1] + 1
                currentMonth += 1

        print(currentDay, currentMonth)

        day = list()
        currentCycle = (dayCount+cycle)%cyclecount
        for j in range(len(timetable[currentCycle])):
            # skip class if free session
            if dictofclass[timetable[currentCycle][j]].name in ("free", "Free"):
                continue
                
            day.append(Event(name=dictofclass[timetable[currentCycle][j]].name,
                             begin=str(currentYear)+"-"+str(currentMonth)+"-"+str(currentDay)+" "+classTimes[j]+"+08:00",
                             duration=classDuration,
                             location=dictofclass[timetable[currentCycle][j]].classroom))
        day.append(Event(name="Day "+str(currentCycle)))

        currentDay += 1
        week.append(day)

    # Adding calendar objects for each day
    for i in range(len(week)):
        for j in week[i]:
            c.events.add(j)

    with open('my.ics', 'w') as my_file:
        my_file.writelines(c)


if __name__ == "__main__":
    main(sys.argv[1:])

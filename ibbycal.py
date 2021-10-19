#!/usr/bin/env python3

from ics import Calendar, Event
import yaml
import sys, getopt
import datetime


class classes:
    def __init__(self, name, classroom, teacher):
        self.name = name
        self.classroom = classroom
        self.teacher = teacher


def usage():
    print("""Usage: ibbycal [OPTION]
               -h, --help   show help
               -c, --cycle  cycle for first day this week
               -y, --year   year of first day this week
               -m, --month  month of first day this week
               -d, --day    day of first day this week
               """)


def main(argv):
    # Parsing arguements
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:y:m:d:", ["help", "cycle=", "year=", "month=", "day="])
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

    # Reading config file
    try:
        with open('config.yaml') as foo:
            data = yaml.safe_load(foo)
    except FileNotFoundError as err:
        print("config not found, exiting")

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

    # Sanity checking
    try:
        cycle
    except NameError:
        print("What's the cycle?: ", end="")
        cycle = int(args)

    try:
        year
    except NameError:
        print("year (enter t for this year): ", end="")

        read = input()
        if read == "t":
            year = datetime.datetime.now().strftime("%Y")
        else:
            year = int(read)

    try:
        month
    except NameError:
        print("month (enter t for this month): ", end="")
        read = input()
        if read == "t":
            month = datetime.datetime.now().strftime("%m")
        else:
            month = int(read)

    try:
        date
    except NameError:
        print("day (enter t for today): ")
        if read == "t":
            date = datetime.datetime.now().strftime("%d")
        else:
            date = int(read)

    if cycle > len(timetable):
        print("cycle is bigger than timetable! Try again.")
        sys.exit(2)

    # recenter cycle so it matches array
    cycle = cycle - 1

    year = str(int(year))
    month = str(int(month))
    date = int(date)

    # Begin is an arrow object
    classTimes = ["08:25:00", "10:00:00", "11:25:00", "14:05:00"]
    # May be set to anything that timedelta() understands/May be set with a dict
    classDuration = {"hours": 1, "minutes": 20}

    c = Calendar()
    week = list()
    day = 10      # temporary work around until time package
    cyclecount = len(timetable)

    for i in range(5):  # A week
        day = list()
        for j in range(len(timetable[0])):
            day.append(Event(name=dictofclass[timetable[(i+cycle)%cyclecount][j]].name,
                             begin=year+"-"+month+"-"+str(date+i)+" "+classTimes[j]+"+08:00",
                             duration=classDuration,
                             location=dictofclass[timetable[(i+cycle)%cyclecount][j]].classroom))
        week.append(day)

    # Adding calendar objects for each day
    for i in range(len(week)):
        for j in range(len(day)):
            c.events.add(week[i][j])

    with open('my.ics', 'w') as my_file:
        my_file.writelines(c)


if __name__ == "__main__":
    main(sys.argv[1:])

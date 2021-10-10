#!/usr/bin/env python3

from ics import Calendar, Event
import yaml
import sys, getopt


class classes:
    def __init__(self, name, classroom, teacher):
        self.name = name
        self.classroom = classroom
        self.teacher = teacher


def usage():
    print("""Usage: ibbycal [OPTION]
               -h, --help   show help
               -d, --cycle  cycle for first day of this week""")


def main(argv):
    # Parsing arguements
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "cycle="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        usage()
        sys.exit(2)

    for opts, args in opts:
        if opts in ("-h", "--help"):
            usage()
        elif opts in ("-d", "--cycle"):
            cycle = int(args)

    # Reading config file
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

    # Sanity checking
    try:
        cycle
    except NameError:
        print("Require cycle option")
        usage()
        sys.exit(2)
    else:
        if cycle > len(timetable):
            print("cycle is bigger than timetable! Try again.")
            sys.exit(2)

    # Begin is an arrow object
    classTimes = ["08:25:00", "10:00:00", "11:25:00", "14:05:00"]
    # May be set to anything that timedelta() understands/May be set with a dict
    classDuration = {"hours": 1, "minutes": 20}

    c = Calendar()
    week = list()
    startDate = 10      # temporary work around until time package
    cyclecount = len(timetable)

    for i in range(5):  # A week
        day = list()
        for j in range(len(timetable[0])):
            day.append(Event(name=dictofclass[timetable[i%cyclecount][j]].name,
                begin='2021-10-'+str(startDate+i)+' '+classTimes[j]+'+08:00',
                             duration=classDuration,
                             location=dictofclass[timetable[i%cyclecount][j]].classroom))
        week.append(day)

    # Adding calendar objects for each day
    for i in range(len(week)):
        for j in range(len(day)):
            c.events.add(week[i][j])

    with open('my.ics', 'w') as my_file:
        my_file.writelines(c)


if __name__ == "__main__":
    main(sys.argv[1:])

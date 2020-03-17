#!/usr/bin/python3
from datetime import datetime
import os, sys


def printHelp():
    print("""timeCalc.py <start_time> <end_time>""")
    pass


def calc(s1, s2):
    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    hours = tdelta.total_seconds() / 3600.
    return tdelta, hours

if __name__ == '__main__':
    if len(sys.argv) < 3 :
        printHelp()
        exit(1)

    s1 = sys.argv[1]
    s2 = sys.argv[2]

    FMT = '%H:%M'
    tdelta, hours = calc(s1, s2)

    print(tdelta, hours)
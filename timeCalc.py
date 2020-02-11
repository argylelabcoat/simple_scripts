#!/usr/bin/python3
from datetime import datetime
import os, sys
s1 = sys.argv[1]
s2 = sys.argv[2]

FMT = '%H:%M'

tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)

hours = tdelta.total_seconds() / 3600.

print(tdelta, hours)
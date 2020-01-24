#!/usr/bin/python3
from datetime import datetime 
now = datetime.now()
name = "{year:04}{month:02}{day:02}-{hour:02}{minute:02}".format(
    year=now.year,
    month=now.month,
    day=now.day,
    hour = now.hour,
    minute = now.minute)
print(name)
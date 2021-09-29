import datetime
import os

d = os.path.getmtime('00.mp3')
date_added = datetime.datetime.fromtimestamp(d)
m = datetime.datetime.timestamp(date_added)
print(d, m)
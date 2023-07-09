import ntplib
from time import ctime
c = ntplib.NTPClient()
response = c.request('x.x.x.21')
print(ctime(response.tx_time))


"""import ntplib 
import time

ntptime.host = "x.x.x.21"
ntptime.settime()
print(time.datetime())"""

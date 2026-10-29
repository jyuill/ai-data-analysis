"""test.py
Simple test with basic function to show time for given time zone. 
run from arrow icon or python test.py
"""

from datetime import datetime
from zoneinfo import ZoneInfo

def get_current_time(timezone):
    """Returns current time for given time zone """
    timezone = ZoneInfo(timezone)
    return datetime.now(timezone).strftime("%H:%M:%S")

ptm = "Time in"

tm1 = "Pacific/Auckland"
tm = get_current_time(tm1)
print(f"{ptm} {tm1}: {tm}")

tm2 = "America/Vancouver"
tm = get_current_time(tm2)

print(f"{ptm} {tm2}: {tm}")
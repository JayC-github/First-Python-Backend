# pylint: disable=C0301
'''
################## time_stamp.py ###################
A simple file to convert datetime object into a unix timestamp
'''

from datetime import datetime
from datetime import timezone
from datetime import timedelta

def get_timestamp_now():
    """
    A function to get the current timestamp in UTC
    Output:
    - (int) timestamp in UTC
    """
    dt_now = datetime.now(timezone.utc)
    #print (dt)
    timestamp = dt_now.timestamp()
    return timestamp

def calculate_time_end(length):
    """
    A function to get a time stamp a certain seconds away from now
    Input:
    - (int) length of the time difference from now
    Output:
    - (int) the timestamp of the time in the future
    """
    dt_now = datetime.now(timezone.utc)
    new_dt = dt_now + timedelta(seconds=length)
    timestamp = new_dt.timestamp()
    return timestamp

if __name__ == "__main__":
    print(get_timestamp_now())

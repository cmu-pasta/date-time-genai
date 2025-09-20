
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
import math # For math.floor
def convert_date_to_julian_day_number(dt: datetime) -> int:
    """
    Converts a datetime object to its Julian Day Number.

    The Julian Day Number (JDN) is an integer number of days that have
    elapsed since noon Universal Time on January 1, 4713 BCE (proleptic
    Julian calendar). This calculation specifically provides the JDN
    for midnight (00:00 UT) of the given Gregorian date.

    Args:
        dt: The input datetime object.

    Returns:
        The Julian Day Number as an integer.
    """
    year = dt.year
    month = dt.month
    day = dt.day

    # Apply the standard algorithm for Gregorian calendar to Julian Day Number
    # This formula is for the JDN at midnight UT.
    a = math.floor((14 - month) / 12)
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    jdn = day + math.floor((153 * m + 2) / 5) + 365 * y + \
          math.floor(y / 4) - math.floor(y / 100) + math.floor(y / 400) - 32045
    
    return jdn

# Entry point: convert_date_to_julian_day_number(dt: datetime) -> int

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_10_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_date_to_julian_day_number(dt):
    result = convert_date_to_julian_day_number(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

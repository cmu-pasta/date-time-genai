
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def is_leap_year(year: int) -> bool:
    # Leap year logic according to Gregorian calendar
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def find_last_leap_day(dt: date) -> date:
    # Step 1: If current year is leap and date is on or after Feb 29, return Feb 29 of this year
    if is_leap_year(dt.year):
        leap_day = date(dt.year, 2, 29)
        if dt >= leap_day:
            return leap_day
    
    # Step 2: Search backward for the previous leap year
    year = dt.year - 1 if dt.month > 2 or (dt.month == 2 and dt.day >= 29) else dt.year - 1
    while year >= 4:
        if is_leap_year(year):
            return date(year, 2, 29)
        year -= 1

    # Step 3: No leap day possible prior to year 4
    raise ValueError("No leap day exists before year 4 in the Gregorian calendar.")

# Entry point: find_last_leap_day(dt: date) -> date

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_95txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_find_last_leap_day(dt):
    result = find_last_leap_day(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

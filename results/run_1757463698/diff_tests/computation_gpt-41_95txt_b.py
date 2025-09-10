
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def is_leap_year(year: int) -> bool:
    # Step 2: Check if the provided year is a leap year
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def last_leap_day_on_or_before(input_date: date) -> date or None:
    # Step 3: Iteratively search for the most recent leap day
    year = input_date.year
    while year >= 1:  # Date module does not support year 0 or BCE
        if is_leap_year(year):
            leap_day = date(year, 2, 29)
            if leap_day <= input_date:
                # Step 4: Return the last Feb 29 found <= input_date
                return leap_day
        year -= 1
    # Step 5: If never found, return None
    return None

# Entry point: last_leap_day_on_or_before(input_date: date) -> date or None

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_95txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_last_leap_day_on_or_before(input_date):
    result = last_leap_day_on_or_before(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")

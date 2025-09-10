
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def days_left_in_quarter(dt: date) -> int:
    # Step 1: Identify the quarter
    year = dt.year
    if dt.month <= 3:  # Q1
        quarter_end = date(year, 3, 31)
    elif dt.month <= 6:  # Q2
        quarter_end = date(year, 6, 30)
    elif dt.month <= 9:  # Q3
        quarter_end = date(year, 9, 30)
    else:  # Q4
        quarter_end = date(year, 12, 31)
    
    # Step 2: Calculate the number of days left (excluding the given day if desired)
    days_left = (quarter_end - dt).days
    
    return days_left

# Entry point: days_left_in_quarter(dt: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_29txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_days_left_in_quarter(dt):
    result = days_left_in_quarter(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

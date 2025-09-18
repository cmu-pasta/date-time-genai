
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_week_number(dt: datetime) -> int:
    # Step 1: Use isocalendar() to get the ISO week number
    # isocalendar() returns a tuple (year, week, weekday)
    iso_calendar = dt.isocalendar()
    
    # Step 2: Extract the week number (second element of the tuple)
    week_number = iso_calendar[1]
    
    # Step 3: Return the week number as an integer
    return week_number

# Entry point: calculate_week_number(dt: datetime) -> int

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_12txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_week_number(dt):
    result = calculate_week_number(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

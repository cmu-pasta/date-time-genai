
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def is_weekend(date_to_check: datetime) -> bool:
    # Step 1: Get the day of the week.
    # weekday() returns an integer: Monday=0, Tuesday=1, ..., Saturday=5, Sunday=6.
    day_of_week = date_to_check.weekday()
    
    # Step 2: Check if the day of the week corresponds to Saturday (5) or Sunday (6).
    if day_of_week == 5 or day_of_week == 6:
        return True
    else:
        return False

# Entry point: is_weekend(date_to_check: datetime) -> bool

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_43_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_is_weekend(date_to_check):
    result = is_weekend(date_to_check)
    formatted_result = format_value_dt(result, date_to_check)
    log_file.write(formatted_result + "\n")

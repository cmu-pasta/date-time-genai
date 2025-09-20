
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def get_week_of_year(dt: datetime) -> int:
    # Step 1: Get the ISO calendar data for the given datetime object.
    # The isocalendar() method returns a named tuple (year, week, weekday).
    iso_calendar_data = dt.isocalendar()
    
    # Step 2: Extract the week number from the ISO calendar data.
    # The 'week' attribute directly gives the ISO week number (1-53).
    week_number = iso_calendar_data.week
    
    # Step 3: Return the week number as an integer.
    return week_number

# Entry point: get_week_of_year(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_82_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_week_of_year(dt):
    result = get_week_of_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def is_leap_year(year: int) -> bool:
    # Step 1: Create a date object for March 1st of the given year.
    # We use 3 for March and 1 for the day.
    march_first = date(year, 3, 1)
    
    # Step 2: Subtract one day to get the last day of February for that year.
    last_day_of_february = march_first - timedelta(days=1)
    
    # Step 3: Check the day component of the resulting date.
    # If it's 29, it's a leap year. Otherwise, it's 28 for a common year.
    return last_day_of_february.day == 29

# Entry point: is_leap_year(year: int) -> bool

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_7_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_is_leap_year(year):
    result = is_leap_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

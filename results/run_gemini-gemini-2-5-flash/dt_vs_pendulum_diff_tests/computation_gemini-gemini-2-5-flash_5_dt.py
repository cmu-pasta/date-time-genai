
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_first_monday(year: int, month: int) -> datetime:
    # Step 1: Create a datetime object for the first day of the given month and year
    first_day_of_month = datetime(year, month, 1)
    
    # Step 2: Get the weekday of the first day of the month
    # Monday is 0, Tuesday is 1, ..., Sunday is 6
    first_day_weekday = first_day_of_month.weekday()
    
    # Step 3: Calculate how many days to add to reach the first Monday
    # (0 - first_day_weekday + 7) % 7 gives the number of days to add to get to the *next* Monday
    # If first_day_weekday is 0 (Monday), days_to_add = (0 - 0 + 7) % 7 = 0
    # If first_day_weekday is 1 (Tuesday), days_to_add = (0 - 1 + 7) % 7 = 6
    # If first_day_weekday is 6 (Sunday), days_to_add = (0 - 6 + 7) % 7 = 1
    days_to_add = (0 - first_day_weekday + 7) % 7
    
    # Step 4: Add the calculated days to the first day of the month
    first_monday = first_day_of_month + timedelta(days=days_to_add)
    
    # Step 5: Return the resulting datetime object
    return first_monday

# Entry point: find_first_monday(year: int, month: int) -> datetime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_5_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_find_first_monday(year, month):
    result = find_first_monday(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")

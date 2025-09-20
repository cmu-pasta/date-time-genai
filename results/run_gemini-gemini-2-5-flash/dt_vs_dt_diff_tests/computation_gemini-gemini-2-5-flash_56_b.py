
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_next_valentines_day(given_date: datetime) -> datetime:
    # Step 1: Get the year of the given date
    year = given_date.year

    # Step 2: Create a datetime object for Valentine's Day of the current year (Feb 14th, 00:00:00)
    # This sets the time to midnight for the start of the day.
    valentines_day_this_year = datetime(year, 2, 14, 0, 0, 0)

    # Step 3: Compare the given_date with Valentine's Day of the current year
    # If the given_date is on or after this year's Valentine's Day,
    # then the next Valentine's Day is in the next calendar year.
    if given_date >= valentines_day_this_year:
        next_year = year + 1
    else:
        # Otherwise, the next Valentine's Day is in the current year.
        next_year = year

    # Step 4: Construct the datetime object for the next Valentine's Day
    next_valentines_day_date = datetime(next_year, 2, 14, 0, 0, 0)
    
    # Step 5: Return the result
    return next_valentines_day_date

# Entry point: find_next_valentines_day(given_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_56_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_valentines_day(given_date):
    result = find_next_valentines_day(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

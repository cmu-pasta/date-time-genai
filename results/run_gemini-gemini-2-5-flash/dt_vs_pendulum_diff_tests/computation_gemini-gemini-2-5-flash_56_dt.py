
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_next_valentines_day(given_date: datetime) -> datetime:
    # Step 1: Construct Valentine's Day for the year of the given_date.
    # We set the time to 00:00:00 for a consistent day-based comparison.
    valentines_this_year = datetime(given_date.year, 2, 14)
    
    # Step 2: Compare the constructed Valentine's Day with the given_date.
    # If the given_date is before or on the Valentine's Day of its year,
    # then this year's Valentine's Day is the next one.
    if given_date <= valentines_this_year:
        return valentines_this_year
    else:
        # Step 3: If the given_date is after Valentine's Day of its year,
        # then the next Valentine's Day is in the following year.
        valentines_next_year = datetime(given_date.year + 1, 2, 14)
        return valentines_next_year

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_56_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_valentines_day(given_date):
    result = find_next_valentines_day(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

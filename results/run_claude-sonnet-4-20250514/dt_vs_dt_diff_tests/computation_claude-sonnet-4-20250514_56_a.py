
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_next_valentines_day(given_date: datetime) -> datetime:
    # Get the year of the given date
    year = given_date.year
    
    # Create Valentine's Day for the current year (February 14th)
    valentines_this_year = datetime(year, 2, 14)
    
    # If the given date is before Valentine's Day this year, return this year's Valentine's Day
    if given_date < valentines_this_year:
        return valentines_this_year
    else:
        # Otherwise, return next year's Valentine's Day
        return datetime(year + 1, 2, 14)

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_56_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_valentines_day(given_date):
    result = find_next_valentines_day(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

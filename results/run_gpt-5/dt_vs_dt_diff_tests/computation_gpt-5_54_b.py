
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_year_progress(dt: datetime) -> float:
    # Determine the start of the year and the start of the next year, preserving tzinfo
    year_start = datetime(dt.year, 1, 1, tzinfo=dt.tzinfo)
    next_year_start = datetime(dt.year + 1, 1, 1, tzinfo=dt.tzinfo)
    
    # Compute total seconds in the year and elapsed seconds since year start
    total_seconds_in_year = (next_year_start - year_start).total_seconds()
    elapsed_seconds = (dt - year_start).total_seconds()
    
    # Calculate percentage of the year that has passed
    percentage = (elapsed_seconds / total_seconds_in_year) * 100.0
    return percentage

# Entry point: calculate_year_progress(dt: datetime) -> float

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_54_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_progress(dt):
    result = calculate_year_progress(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

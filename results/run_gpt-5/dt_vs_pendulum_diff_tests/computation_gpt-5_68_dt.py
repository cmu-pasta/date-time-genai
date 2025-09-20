
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_labor_day(year: int) -> date:
    # Step 1: Start at September 1st of the given year
    sept_first = date(year, 9, 1)
    # Step 2: Calculate weekday (Monday=0, Sunday=6)
    weekday = sept_first.weekday()
    # Step 3: Compute days to the first Monday
    days_to_monday = (7 - weekday) % 7
    # Step 4: Determine Labor Day date
    labor_day = sept_first + timedelta(days=days_to_monday)
    return labor_day

# Entry point: find_labor_day(year: int) -> date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_68_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_labor_day(year):
    result = find_labor_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

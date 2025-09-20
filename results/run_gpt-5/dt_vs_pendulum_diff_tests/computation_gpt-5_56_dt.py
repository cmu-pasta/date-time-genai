
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def next_valentines_day(d: date) -> date:
    # Step 1: Determine Valentine's Day for the current year
    valentines_this_year = date(d.year, 2, 14)
    # Step 2: If the given date is on/after Feb 14, return next year's Feb 14; else this year's
    target_year = d.year + 1 if d >= valentines_this_year else d.year
    # Step 3: Construct and return the result
    return date(target_year, 2, 14)

# Entry point: next_valentines_day(d: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_56_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_valentines_day(d):
    result = next_valentines_day(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")

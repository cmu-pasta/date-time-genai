
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def next_valentines_day(current_date: date) -> date:
    """
    Return the next Valentine's Day (February 14) strictly after the given date.
    If current_date is before Feb 14 of its year, returns Feb 14 of the same year.
    If current_date is on or after Feb 14, returns Feb 14 of the next year.
    """
    valentines_this_year = date(current_date.year, 2, 14)
    if current_date < valentines_this_year:
        return valentines_this_year
    else:
        return date(current_date.year + 1, 2, 14)

# Entry point: next_valentines_day(current_date: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_56_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_valentines_day(current_date):
    result = next_valentines_day(current_date)
    formatted_result = format_value_dt(result, current_date)
    log_file.write(formatted_result + "\n")

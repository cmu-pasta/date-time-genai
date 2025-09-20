
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_buddhist_year(gregorian_date: date) -> int:
    """
    Determine the Buddhist calendar year (B.E.) for a given Gregorian date.

    Parameters:
    - gregorian_date: date (Gregorian calendar date)

    Returns:
    - int: Buddhist calendar year corresponding to the given Gregorian date
    """
    # Buddhist Era year is calculated by adding 543 to the Common Era (Gregorian) year.
    return gregorian_date.year + 543

# Entry point: determine_buddhist_year(gregorian_date: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_79_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_buddhist_year(gregorian_date):
    result = determine_buddhist_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")

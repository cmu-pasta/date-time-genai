
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_season(d: date) -> int:
    """
    Returns the meteorological season code for a given date.
    Season codes:
      1 = Spring (Mar-May)
      2 = Summer (Jun-Aug)
      3 = Autumn (Sep-Nov)
      4 = Winter (Dec-Feb)
    """
    m = d.month
    if m in (3, 4, 5):
        return 1  # Spring
    if m in (6, 7, 8):
        return 2  # Summer
    if m in (9, 10, 11):
        return 3  # Autumn
    return 4  # Winter (Dec, Jan, Feb)

# Entry point: determine_season(d: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_19_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_season(d):
    result = determine_season(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")

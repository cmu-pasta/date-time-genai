
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_season(input_date: date) -> int:
    """
    Determine the meteorological season (Northern Hemisphere) for a given date.
    Returns an integer code:
      1 = spring (Mar 1 - May 31)
      2 = summer (Jun 1 - Aug 31)
      3 = autumn (Sep 1 - Nov 30)
      4 = winter (Dec 1 - Feb 28/29)
    """
    month = input_date.month

    if month in (3, 4, 5):
        return 1  # spring
    elif month in (6, 7, 8):
        return 2  # summer
    elif month in (9, 10, 11):
        return 3  # autumn
    else:
        return 4  # winter

# Entry point: determine_season(input_date: date) -> int

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_19txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_season(input_date):
    result = determine_season(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")

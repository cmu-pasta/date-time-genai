
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def previous_friday_before(d: date) -> date:
    """
    Return the previous Friday strictly before the given date.
    If the given date is a Friday, returns the Friday one week earlier.
    """
    weekday = d.weekday()  # Monday=0 ... Sunday=6
    days_back = (weekday - 4) % 7  # distance to Friday (4)
    if days_back == 0:
        days_back = 7  # ensure strictly previous Friday
    return d - timedelta(days=days_back)

# Entry point: previous_friday_before(d: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_20_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_previous_friday_before(d):
    result = previous_friday_before(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")

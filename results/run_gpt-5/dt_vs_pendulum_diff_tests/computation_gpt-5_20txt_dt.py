
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def previous_friday(d: date) -> date:
    """
    Return the previous Friday strictly before the given date.
    Friday is considered weekday 4 (Monday=0 ... Sunday=6).
    """
    # Days since the most recent Friday (0 if Friday, 1 if Saturday, ..., 6 if Thursday)
    days_since_friday = (d.weekday() - 4) % 7
    # If the given date is Friday, move back 7 days to get the previous Friday
    days_to_subtract = days_since_friday if days_since_friday != 0 else 7
    return d - timedelta(days=days_to_subtract)

# Entry point: previous_friday(d: date) -> date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_20txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_previous_friday(d):
    result = previous_friday(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")

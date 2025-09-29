
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def convert_date_to_week(d: date) -> int:
    """
    Convert a date to its ISO week number (1-53).
    """
    # ISO week number: Monday as the first day of the week, weeks starting with the first Thursday of the year
    week_number = d.isocalendar().week
    return int(week_number)

# Entry point: convert_date_to_week(d: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_82txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_convert_date_to_week(d):
    result = convert_date_to_week(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")

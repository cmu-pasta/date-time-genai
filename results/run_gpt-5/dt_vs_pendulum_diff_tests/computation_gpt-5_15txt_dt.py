
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_weekend_days(start_date: date, end_date: date) -> int:
    """
    Calculate the number of weekend days (Saturdays and Sundays) between two dates, inclusive.

    Args:
        start_date (date): The start date.
        end_date (date): The end date.

    Returns:
        int: The number of weekend days between start_date and end_date inclusive.
    """
    # Ensure chronological order
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    # Inclusive day count
    total_days = (end_date - start_date).days + 1

    # Weekend days from full weeks
    full_weeks = total_days // 7
    weekend_days = full_weeks * 2

    # Remaining days after full weeks
    remaining_days = total_days % 7
    start_wd = start_date.weekday()  # 0=Mon, ..., 5=Sat, 6=Sun

    # Count weekend days in the remaining segment
    for i in range(remaining_days):
        wd = (start_wd + i) % 7
        if wd == 5 or wd == 6:  # Saturday or Sunday
            weekend_days += 1

    return weekend_days

# Entry point: count_weekend_days(start_date: date, end_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_15txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_weekend_days(start_date, end_date):
    result = count_weekend_days(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")

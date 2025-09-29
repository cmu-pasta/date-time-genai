
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def last_weekday_of_month(year: int, month: int, weekday: int) -> date:
    """
    Find the last occurrence of a specific weekday in a given month.

    Parameters:
    - year: integer year (e.g., 2025)
    - month: integer month in 1..12
    - weekday: integer weekday where Monday=0 ... Sunday=6

    Returns:
    - date: the date of the last occurrence of the specified weekday in the given month
    """
    if not (1 <= month <= 12):
        raise ValueError("month must be in 1..12")
    if not (0 <= weekday <= 6):
        raise ValueError("weekday must be in 0..6 with Monday=0 and Sunday=6")

    # Step 1: Compute the first day of the next month
    if month == 12:
        next_month_first = date(year + 1, 1, 1)
    else:
        next_month_first = date(year, month + 1, 1)

    # Step 2: Last day of the given month
    last_day = next_month_first - timedelta(days=1)

    # Step 3: Offset back to the desired weekday
    offset = (last_day.weekday() - weekday) % 7

    # Step 4: Compute the target date
    result = last_day - timedelta(days=offset)
    return result

# Entry point: last_weekday_of_month(year: int, month: int, weekday: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_80txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_last_weekday_of_month(year, month, weekday):
    result = last_weekday_of_month(year, month, weekday)
    formatted_result = format_value_dt(result, year, month, weekday)
    log_file.write(formatted_result + "\n")

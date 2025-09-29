
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_trading_days(year: int) -> int:
    """
    Calculate the number of trading days (weekdays: Monday–Friday) in a given year.

    Parameters:
        year (int): The year for which to count trading days.

    Returns:
        int: The number of trading days in the specified year.
    """
    start = date(year, 1, 1)
    end = date(year, 12, 31)

    total_days = (end - start).days + 1
    trading_days = 0

    current = start
    for _ in range(total_days):
        # Monday=0, Sunday=6
        if current.weekday() < 5:
            trading_days += 1
        current += timedelta(days=1)

    return trading_days

# Entry point: count_trading_days(year: int) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_66txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_trading_days(year):
    result = count_trading_days(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

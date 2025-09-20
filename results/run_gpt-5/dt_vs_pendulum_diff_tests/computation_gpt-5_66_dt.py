
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_trading_days_in_year(year: int) -> int:
    """
    Calculate the number of trading days (weekdays, Monday-Friday) in a given year.
    
    Args:
        year (int): The year for which to compute trading days.
    
    Returns:
        int: The count of trading days in the specified year.
    """
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    one_day = timedelta(days=1)
    
    trading_days = 0
    current = start
    while current <= end:
        # weekday(): Monday=0, Sunday=6; trading days are Monday(0) to Friday(4)
        if current.weekday() < 5:
            trading_days += 1
        current += one_day
    
    return trading_days

# Entry point: calculate_trading_days_in_year(year: int) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_66_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_trading_days_in_year(year):
    result = calculate_trading_days_in_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_trading_days(year: int) -> int:
    """
    Calculates the number of trading days (weekdays from Monday to Friday)
    in a given year using only the datetime library.
    
    Args:
        year (int): The year for which to calculate trading days.

    Returns:
        int: The number of weekdays (trading days) in the specified year.
    """
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    
    trading_days_count = 0
    current_date = start_date

    # Iterate through each day of the year
    while current_date <= end_date:
        # Check if the current day is a weekday (Monday=0 to Friday=4)
        if 0 <= current_date.weekday() <= 4:
            trading_days_count += 1
        
        # Move to the next day
        current_date += timedelta(days=1)
            
    return trading_days_count

# Entry point: calculate_trading_days(year: int) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_66_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_trading_days(year):
    result = calculate_trading_days(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

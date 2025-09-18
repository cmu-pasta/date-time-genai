
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_trading_days_in_year(year: int) -> int:
    # Step 1: Create start and end dates for the given year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    
    # Step 2: Initialize trading days counter
    trading_days = 0
    
    # Step 3: Iterate through all days in the year
    current_date = start_date
    while current_date <= end_date:
        # Step 4: Check if current day is a weekday (Monday=0 to Friday=4)
        if current_date.weekday() < 5:  # 0-4 are weekdays, 5-6 are weekends
            trading_days += 1
        
        # Step 5: Move to the next day
        current_date += timedelta(days=1)
    
    # Step 6: Return the total count of trading days
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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_66txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_trading_days_in_year(year):
    result = calculate_trading_days_in_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

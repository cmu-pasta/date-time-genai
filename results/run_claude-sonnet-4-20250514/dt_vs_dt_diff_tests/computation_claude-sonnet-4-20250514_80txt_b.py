
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import calendar
def find_last_weekday_in_month(dt: datetime, target_weekday: int) -> datetime:
    # Step 1: Extract year and month from the input datetime
    year = dt.year
    month = dt.month
    
    # Step 2: Find the last day of the month
    last_day_of_month = calendar.monthrange(year, month)[1]
    
    # Step 3: Create a datetime object for the last day of the month
    last_date = datetime(year, month, last_day_of_month)
    
    # Step 4: Work backwards from the last day to find the target weekday
    current_date = last_date
    while current_date.weekday() != target_weekday:
        current_date = current_date - timedelta(days=1)
        # Safety check to ensure we don't go before the first day of the month
        if current_date.month != month:
            # This should never happen for valid weekdays, but just in case
            break
    
    # Step 5: Return the result
    return current_date

# Entry point: find_last_weekday_in_month(dt: datetime, target_weekday: int) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_80txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy())
def test_find_last_weekday_in_month(dt, target_weekday):
    result = find_last_weekday_in_month(dt, target_weekday)
    formatted_result = format_value_dt(result, dt, target_weekday)
    log_file.write(formatted_result + "\n")

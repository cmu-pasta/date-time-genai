
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def last_weekday_in_month(year: int, month: int, weekday: int) -> date:
    """
    Returns the date of the last occurrence of a specific weekday in a given month.
    
    Parameters:
    - year: The year as an integer.
    - month: The month as an integer (1-12).
    - weekday: The target weekday as an integer, where Monday is 0 and Sunday is 6.
    
    Returns:
    - A date object representing the last occurrence of the specified weekday in the given month.
    """
    # Step 1: Find the last day of the month
    if month == 12:
        last_day = date(year, 12, 31)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    # Step 2: Iterate backwards to find the last occurrence of the specified weekday
    days_to_subtract = (last_day.weekday() - weekday) % 7
    target_date = last_day - timedelta(days=days_to_subtract)
    
    # Step 3: Return the target date
    return target_date

# Entry point: last_weekday_in_month(year: int, month: int, weekday: int) -> date

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_55txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_last_weekday_in_month(year, month, weekday):
    result = last_weekday_in_month(year, month, weekday)
    formatted_result = format_value_dt(result, year, month, weekday)
    log_file.write(formatted_result + "\n")

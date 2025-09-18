
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date:
    """
    Find the nth occurrence of a specific weekday in a given month.
    
    Args:
        year: The year (integer)
        month: The month (1-12)
        weekday: The target weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)
        n: Which occurrence to find (1st, 2nd, 3rd, etc.)
    
    Returns:
        date: The date of the nth occurrence of the weekday
    """
    # Start from the first day of the month
    current_date = date(year, month, 1)
    
    # Calculate the last day of the month
    if month == 12:
        next_month_first = date(year + 1, 1, 1)
    else:
        next_month_first = date(year, month + 1, 1)
    
    last_day_of_month = next_month_first - timedelta(days=1)
    
    # Count occurrences of the target weekday
    occurrence_count = 0
    
    # Iterate through each day of the month
    while current_date <= last_day_of_month:
        # Check if current day matches the target weekday
        if current_date.weekday() == weekday:
            occurrence_count += 1
            # If we've found the nth occurrence, return this date
            if occurrence_count == n:
                return current_date
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    # If nth occurrence doesn't exist, return the last day of the month
    # (This handles edge cases where nth occurrence doesn't exist)
    return last_day_of_month

# Entry point: find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_17txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, weekday, n):
    result = find_nth_weekday_in_month(year, month, weekday, n)
    formatted_result = format_value_dt(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")

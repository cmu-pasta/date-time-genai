
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> date:
    """
    Find the nth occurrence of a specific weekday in a given month.
    
    Args:
        year: The year (integer)
        month: The month (1-12)
        weekday: The target weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)
        n: Which occurrence to find (1st, 2nd, 3rd, etc.)
    
    Returns:
        date object of the nth occurrence, or None if it doesn't exist
    """
    # Step 1: Get the first day of the month
    first_day = date(year, month, 1)
    
    # Step 2: Find what day of the week the first day is
    first_weekday = first_day.weekday()  # 0=Monday, 6=Sunday
    
    # Step 3: Calculate days to add to reach the first occurrence of target weekday
    days_to_first_occurrence = (weekday - first_weekday) % 7
    
    # Step 4: Calculate the date of the first occurrence
    first_occurrence = date(year, month, 1 + days_to_first_occurrence)
    
    # Step 5: Calculate the nth occurrence by adding (n-1) weeks
    nth_occurrence_day = first_occurrence.day + (n - 1) * 7
    
    # Step 6: Check if the nth occurrence is still within the same month
    try:
        nth_occurrence = date(year, month, nth_occurrence_day)
        # Verify it's still the same month (this check handles month boundary issues)
        if nth_occurrence.month == month:
            return nth_occurrence
        else:
            return None
    except ValueError:
        # Day is out of range for the month
        return None

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_17txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, weekday, n):
    result = find_nth_weekday_in_month(year, month, weekday, n)
    formatted_result = format_value_dt(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")

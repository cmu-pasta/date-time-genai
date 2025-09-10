
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_weekday_in_month(year: int, month: int, weekday: int) -> int:
    """
    Counts the number of times a specific weekday occurs in a given month and year.

    Args:
        year (int): The year as a 4-digit integer (e.g., 2024).
        month (int): The month as an integer (1=January, ..., 12=December).
        weekday (int): The weekday as an integer, where Monday is 0 and Sunday is 6.

    Returns:
        int: The total number of dates in the specified month that fall on the given weekday.
    """
    # Step 1: Find the first day of the month
    first_day = date(year, month, 1)
    first_day_weekday = first_day.weekday()
    
    # Step 2: Calculate days to add to reach the first desired weekday
    delta_days = (weekday - first_day_weekday) % 7
    first_occurrence = first_day + timedelta(days=delta_days)
    
    # Step 3: Iterate each week, counting the occurrences
    count = 0
    current = first_occurrence
    while current.month == month:
        count += 1
        current += timedelta(days=7)
    
    # Step 4: Return the total count as integer
    return count

# Entry point: count_weekday_in_month(year: int, month: int, weekday: int) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_77txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_count_weekday_in_month(year, month, weekday):
    result = count_weekday_in_month(year, month, weekday)
    formatted_result = format_value_dt(result, year, month, weekday)
    log_file.write(formatted_result + "\n")

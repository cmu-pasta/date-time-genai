
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def get_nth_sunday(year: int, month: int, n: int) -> date:
    """
    Returns the date of the nth Sunday of the specified month and year.
    If there is no nth Sunday in the month, returns None.
    """
    # Step 1: Find the first day of the month
    first_day = date(year, month, 1)
    
    # Step 2: Calculate the weekday of the first day (Monday=0, Sunday=6)
    first_day_weekday = first_day.weekday()
    
    # Step 3: Calculate days to add to get the first Sunday
    days_until_sunday = (6 - first_day_weekday) % 7
    first_sunday = first_day + timedelta(days=days_until_sunday)
    
    # Step 4: Calculate the nth Sunday
    nth_sunday = first_sunday + timedelta(days=7*(n-1))
    
    # Step 5: Validate if nth_sunday is still within the same month
    if nth_sunday.month == month:
        return nth_sunday
    else:
        return None

# Entry point: get_nth_sunday(year: int, month: int, n: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_52txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_get_nth_sunday(year, month, n):
    result = get_nth_sunday(year, month, n)
    formatted_result = format_value_dt(result, year, month, n)
    log_file.write(formatted_result + "\n")

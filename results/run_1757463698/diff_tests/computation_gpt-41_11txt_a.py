
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """
    Find the date of the nth occurrence of a weekday in a given month and year.
    - year: int (e.g., 2024)
    - month: int (1=January, ..., 12=December)
    - weekday: int (0=Monday, ..., 6=Sunday)
    - n: int (nth occurrence, e.g., 2 for 2nd Wednesday)
    Returns:
        If the nth weekday exists, return the date as a datetime.date object.
        If not, return None.
    """
    # Step 1: Get the first day of the month
    first_day = date(year, month, 1)
    first_day_weekday = first_day.weekday()  # 0=Monday, 6=Sunday

    # Step 2: Calculate days until first occurrence of target weekday
    days_until_weekday = (weekday - first_day_weekday + 7) % 7
    first_occurrence = first_day + timedelta(days=days_until_weekday)

    # Step 3: Calculate the nth occurrence
    nth_occurrence = first_occurrence + timedelta(weeks=n-1)
    
    # Step 4: Check if the nth occurrence is still in the same month
    if nth_occurrence.month == month:
        return nth_occurrence
    else:
        return None

# Entry point: nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_11txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_nth_weekday_of_month(year, month, weekday, n):
    result = nth_weekday_of_month(year, month, weekday, n)
    formatted_result = format_value_dt(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")

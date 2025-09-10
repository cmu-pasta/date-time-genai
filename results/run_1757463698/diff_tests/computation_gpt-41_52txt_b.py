
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def get_nth_sunday_in_month(year: int, month: int, n: int) -> date:
    """
    Given a year, a month, and an integer n, return the date of the nth Sunday in the month.
    If there are fewer than n Sundays, return date.min.
    """
    if n < 1 or month < 1 or month > 12:
        return date.min  # Invalid input

    # Step 1: Find the first day of the month
    first_day = date(year, month, 1)
    # Step 2: Find the weekday (Monday=0,...,Sunday=6)
    first_day_weekday = first_day.weekday()
    # Step 3: Calculate days to the first Sunday
    days_to_first_sunday = (6 - first_day_weekday) % 7
    first_sunday = first_day + timedelta(days=days_to_first_sunday)

    # Step 4: Calculate the nth Sunday
    nth_sunday = first_sunday + timedelta(days=7*(n-1))
    # Step 5: Check if nth_sunday is in the same month
    if nth_sunday.month != month:
        return date.min  # Not enough Sundays
    return nth_sunday

# Entry point: get_nth_sunday_in_month(year: int, month: int, n: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_52txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_get_nth_sunday_in_month(year, month, n):
    result = get_nth_sunday_in_month(year, month, n)
    formatted_result = format_value_dt(result, year, month, n)
    log_file.write(formatted_result + "\n")

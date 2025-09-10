
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def get_next_nth_weekday(start_date: date, ordinal: int, weekday: int) -> date:
    """
    Returns the next date after start_date that is the given ordinal occurrence
    of the specified weekday in a month.
    
    For example: get_next_nth_weekday(date(2024,6,15), 3, 3) returns the next 3rd Thursday after June 15, 2024.
    """
    # Step 1: Start checking from the month containing the day AFTER start_date
    # If the matching date in the current month is after start_date, use it
    # Otherwise, move to the next month
    
    # Helper to find the nth weekday of a given month/year
    def nth_weekday_of_month(year: int, month: int, ordinal: int, weekday: int) -> date:
        # Find the first occurrence of the weekday in the month
        first_day = date(year, month, 1)
        first_day_wd = first_day.weekday()
        days_until_weekday = (weekday - first_day_wd) % 7
        first_occurrence = first_day + timedelta(days=days_until_weekday)
        # The nth occurrence:
        nth_occurrence = first_occurrence + timedelta(weeks=ordinal-1)
        # Make sure it is in the same month
        if nth_occurrence.month == month:
            return nth_occurrence
        else:
            # It doesn't exist that month
            return None

    # Begin loop to find next matching date
    year = start_date.year
    month = start_date.month

    while True:
        candidate = nth_weekday_of_month(year, month, ordinal, weekday)
        if candidate and candidate > start_date:
            return candidate
        # Move to next month
        month += 1
        if month > 12:
            month = 1
            year += 1

# Entry point: get_next_nth_weekday(start_date: date, ordinal: int, weekday: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_42txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy(), timestamp_strategy())
def test_get_next_nth_weekday(start_date, ordinal, weekday):
    result = get_next_nth_weekday(start_date, ordinal, weekday)
    formatted_result = format_value_dt(result, start_date, ordinal, weekday)
    log_file.write(formatted_result + "\n")

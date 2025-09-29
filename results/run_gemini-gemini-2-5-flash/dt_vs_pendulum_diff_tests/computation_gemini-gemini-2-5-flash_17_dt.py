
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_nth_weekday_in_month(year: int, month: int, weekday_num: int, n: int) -> date | None:
    """
    Finds the nth occurrence of a specific weekday in a given month.

    Args:
        year: The year as an integer (e.g., 2023).
        month: The month as an integer (1-12).
        weekday_num: The target weekday as an integer (0=Monday, 6=Sunday).
        n: The occurrence number (e.g., 1 for the 1st, 2 for the 2nd).

    Returns:
        A datetime.date object representing the nth occurrence, or None if it doesn't exist.
    """
    # Step 1: Create a date object for the first day of the given month
    first_day_of_month = date(year, month, 1)

    # Step 2: Calculate the number of days to add to reach the first occurrence
    # (weekday_num - first_day_of_month.weekday() + 7) % 7 calculates the difference
    # For example:
    # If first_day_of_month is Monday (0) and target is Monday (0), diff = (0 - 0 + 7) % 7 = 0
    # If first_day_of_month is Monday (0) and target is Tuesday (1), diff = (1 - 0 + 7) % 7 = 1
    # If first_day_of_month is Sunday (6) and target is Monday (0), diff = (0 - 6 + 7) % 7 = 1
    days_to_first_occurrence = (weekday_num - first_day_of_month.weekday() + 7) % 7

    # Step 3: Calculate the date of the first occurrence of the target weekday
    first_occurrence_date = first_day_of_month + timedelta(days=days_to_first_occurrence)

    # Step 4: Calculate the date of the nth occurrence
    # We add (n - 1) * 7 days to the first occurrence date
    nth_occurrence_date = first_occurrence_date + timedelta(days=(n - 1) * 7)

    # Step 5: Check if the calculated nth occurrence is still within the original month
    if nth_occurrence_date.month == month:
        return nth_occurrence_date
    else:
        # If the month is different, the nth occurrence does not exist in this month
        return None

# Entry point: find_nth_weekday_in_month(year: int, month: int, weekday_num: int, n: int) -> date | None

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_17_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, weekday_num, n):
    result = find_nth_weekday_in_month(year, month, weekday_num, n)
    formatted_result = format_value_dt(result, year, month, weekday_num, n)
    log_file.write(formatted_result + "\n")

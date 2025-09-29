
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_hours_in_month(dt: datetime) -> int:
    """
    Calculates the total number of hours in the month of the given datetime object,
    considering leap years.

    Args:
        dt: A datetime object representing any day within the target month.

    Returns:
        An integer representing the total number of hours in that month.
    """
    year = dt.year
    month = dt.month

    # Step 1: Get the first day of the current month
    first_day_of_month = datetime(year, month, 1)

    # Step 2: Determine the first day of the next month
    if month == 12:
        # If it's December, the next month is January of the next year
        first_day_of_next_month = datetime(year + 1, 1, 1)
    else:
        # Otherwise, it's the next month in the same year
        first_day_of_next_month = datetime(year, month + 1, 1)

    # Step 3: Calculate the number of days in the month
    # Subtracting two datetime objects results in a timedelta object.
    # The .days attribute of timedelta gives the difference in days.
    num_days = (first_day_of_next_month - first_day_of_month).days

    # Step 4: Calculate the total hours
    total_hours = num_days * 24

    # Step 5: Return the result
    return total_hours

# Entry point: calculate_hours_in_month(dt: datetime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_42_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_hours_in_month(dt):
    result = calculate_hours_in_month(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

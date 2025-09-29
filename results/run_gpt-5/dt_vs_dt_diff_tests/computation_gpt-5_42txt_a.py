
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_hours_in_month(year: int, month: int) -> int:
    """
    Calculate the number of hours in a given month of a specific year,
    correctly accounting for leap years.

    Inputs:
      - year: integer (e.g., 2024)
      - month: integer in [1, 12]

    Output:
      - integer: total hours in the specified month
    """
    # Step 1: Create the date for the first day of the given month
    start_of_month = date(year, month, 1)

    # Step 2: Determine the first day of the next month
    if month == 12:
        start_of_next_month = date(year + 1, 1, 1)
    else:
        start_of_next_month = date(year, month + 1, 1)

    # Step 3: Compute the number of days in the month
    days_in_month = (start_of_next_month - start_of_month).days

    # Step 4: Convert days to hours
    hours_in_month = days_in_month * 24

    # Step 5: Return the total hours as an integer
    return int(hours_in_month)

# Entry point: calculate_hours_in_month(year: int, month: int) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_42txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_calculate_hours_in_month(year, month):
    result = calculate_hours_in_month(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")

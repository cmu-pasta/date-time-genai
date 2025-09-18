
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def hours_in_month(year: int, month: int) -> int:
    """
    Calculate the number of hours in a given month for a specific year,
    correctly accounting for leap years.
    
    Parameters:
        year (int): The year (e.g., 2024)
        month (int): The month (1-12)
    
    Returns:
        int: The number of hours in the specified month.
    """
    # Step 1: Determine the first day of the given month
    start = date(year, month, 1)
    
    # Step 2: Determine the first day of the next month
    if month == 12:
        next_month_start = date(year + 1, 1, 1)
    else:
        next_month_start = date(year, month + 1, 1)
    
    # Step 3: Calculate the difference in days between the two dates
    days_in_month = (next_month_start - start).days
    
    # Step 4: Convert days to hours
    hours = days_in_month * 24
    
    return hours

# Entry point: hours_in_month(year: int, month: int) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_42txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_hours_in_month(year, month):
    result = hours_in_month(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")

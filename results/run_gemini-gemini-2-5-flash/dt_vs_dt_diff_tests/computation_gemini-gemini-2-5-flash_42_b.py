
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_hours_in_month(month_date: date) -> int:
    """
    Calculates the total number of hours in a given month, considering leap years.

    Args:
        month_date: A datetime.date object representing any day within the target month.

    Returns:
        An integer representing the total number of hours in that month.
    """
    # Step 3: Determine the first day of the given month
    first_day_of_month = date(month_date.year, month_date.month, 1)

    # Step 4: Determine the first day of the next month
    if month_date.month == 12:
        first_day_of_next_month = date(month_date.year + 1, 1, 1)
    else:
        first_day_of_next_month = date(month_date.year, month_date.month + 1, 1)
    
    # Step 5: Calculate the number of days in the given month
    # Subtracting the first day of the current month from the first day of the next month
    # gives a timedelta whose 'days' attribute is the number of days in the current month.
    num_days = (first_day_of_next_month - first_day_of_month).days
    
    # Step 6: Calculate the total hours
    total_hours = num_days * 24
    
    # Step 7: Return the result as an integer
    return total_hours

# Entry point: calculate_hours_in_month(month_date: date) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_42_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_hours_in_month(month_date):
    result = calculate_hours_in_month(month_date)
    formatted_result = format_value_dt(result, month_date)
    log_file.write(formatted_result + "\n")

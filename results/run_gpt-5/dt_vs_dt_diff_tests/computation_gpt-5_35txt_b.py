
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def last_business_day(year: int, month: int) -> date:
    """
    Find the last business day (Monday-Friday) of the given month and year.
    
    Args:
        year (int): The year of interest (e.g., 2025).
        month (int): The month of interest as an integer from 1 to 12.
    
    Returns:
        date: The last business day of the given month.
    """
    # Step 1: Get the first day of the next month
    if month == 12:
        first_of_next_month = date(year + 1, 1, 1)
    else:
        first_of_next_month = date(year, month + 1, 1)
    
    # Step 2: The last calendar day of the current month
    last_calendar_day = first_of_next_month - timedelta(days=1)
    
    # Step 3: Adjust backward if the last calendar day is a weekend
    # weekday(): Monday=0 ... Sunday=6
    if last_calendar_day.weekday() >= 5:  # 5=Saturday, 6=Sunday
        days_to_subtract = last_calendar_day.weekday() - 4  # Sat->1, Sun->2
        last_calendar_day -= timedelta(days=days_to_subtract)
    
    # Step 4: Return the last business day
    return last_calendar_day

# Entry point: last_business_day(year: int, month: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_35txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_last_business_day(year, month):
    result = last_business_day(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_business_day_of_month(input_date: datetime) -> datetime:
    # Step 3: Determine the last day of the given month.
    # First, find the year and month from the input_date.
    year = input_date.year
    month = input_date.month

    # Calculate the first day of the next month
    if month == 12:
        # If the current month is December, the next month is January of the next year.
        first_day_of_next_month = datetime(year + 1, 1, 1)
    else:
        # Otherwise, it's the next month in the same year.
        first_day_of_next_month = datetime(year, month + 1, 1)

    # Subtract one day from the first day of the next month to get the last day of the current month.
    last_day_of_month = first_day_of_next_month - timedelta(days=1)

    # Step 4: Iterate backward from the last day until a business day is found.
    current_day = last_day_of_month
    
    # A business day is Monday (0) through Friday (4).
    # We need to skip Saturday (5) and Sunday (6).
    while current_day.weekday() >= 5: # 5 is Saturday, 6 is Sunday
        current_day -= timedelta(days=1)
    
    # Step 5: Return the found business day.
    return current_day

# Entry point: find_last_business_day_of_month(input_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_35_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_business_day_of_month(input_date):
    result = find_last_business_day_of_month(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_day_of_month(input_date: datetime) -> datetime:
    # Step 1: Determine the year and month of the input date
    year = input_date.year
    month = input_date.month

    # Step 2: Calculate the first day of the next month
    if month == 12:
        # If the current month is December, the next month is January of the next year
        next_month_first_day = datetime(year + 1, 1, 1)
    else:
        # Otherwise, the next month is the current month + 1 in the same year
        next_month_first_day = datetime(year, month + 1, 1)
    
    # Step 3: Subtract one day from the first day of the next month
    # This gives us the last day of the current month
    last_day = next_month_first_day - timedelta(days=1)
    
    # Step 4: Return the result
    return last_day

# Entry point: find_last_day_of_month(input_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_8_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_day_of_month(input_date):
    result = find_last_day_of_month(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")

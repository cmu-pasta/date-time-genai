
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Determine the earlier and later dates
    start_date = min(dt1, dt2)
    end_date = max(dt1, dt2)

    business_days_count = 0
    current_date = start_date

    # Step 2: Iterate through each day from start_date to end_date (inclusive)
    # Using timedelta(days=1) to advance by one day at a time
    while current_date <= end_date:
        # Step 3: Check if the current day is a weekday (Monday=0 to Friday=4)
        if 0 <= current_date.weekday() <= 4:
            business_days_count += 1
        
        # Move to the next day
        current_date += timedelta(days=1)
        
    return business_days_count

# Entry point: calculate_business_days(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_0_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_business_days(dt1, dt2):
    result = calculate_business_days(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")

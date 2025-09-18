
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Ensure dt_start is the earlier date and dt_end is the later date.
    # This simplifies the iteration logic.
    if dt1 > dt2:
        dt_start = dt2
        dt_end = dt1
    else:
        dt_start = dt1
        dt_end = dt2

    business_days_count = 0
    current_date = dt_start

    # Step 2: Iterate day by day from the start date to the end date (inclusive).
    # We only care about the date component, so the time part of datetime objects
    # does not affect the business day calculation.
    while current_date <= dt_end:
        # Step 3: Check if the current day is a business day (Monday to Friday).
        # weekday() returns 0 for Monday, 1 for Tuesday, ..., 4 for Friday, 5 for Saturday, 6 for Sunday.
        if current_date.weekday() < 5:  # Monday (0) through Friday (4)
            business_days_count += 1
        
        # Step 4: Move to the next day.
        current_date += timedelta(days=1)
        
    # Step 5: Return the total count of business days.
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

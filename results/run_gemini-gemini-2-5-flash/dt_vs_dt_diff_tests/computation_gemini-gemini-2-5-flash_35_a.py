
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_business_day_of_month(dt: datetime) -> datetime:
    # Step 1: Determine the year and month of the input date
    year = dt.year
    month = dt.month

    # Step 2: Calculate the first day of the next month
    if month == 12:
        # If the current month is December, the next month is January of the next year
        first_day_of_next_month = datetime(year + 1, 1, 1)
    else:
        # Otherwise, the next month is month + 1 in the same year
        first_day_of_next_month = datetime(year, month + 1, 1)

    # Step 3: Subtract one day to get the last day of the current month
    last_day_of_current_month = first_day_of_next_month - timedelta(days=1)

    # Step 4: Iterate backwards from the last day until a business day (Monday-Friday) is found
    # A business day has a weekday value from 0 (Monday) to 4 (Friday).
    # Saturday is 5, Sunday is 6.
    last_business_day = last_day_of_current_month
    while last_business_day.weekday() >= 5: # While it's Saturday (5) or Sunday (6)
        last_business_day -= timedelta(days=1)

    # Step 5: Return the found last business day
    return last_business_day

# Entry point: find_last_business_day_of_month(dt: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_35_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_business_day_of_month(dt):
    result = find_last_business_day_of_month(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

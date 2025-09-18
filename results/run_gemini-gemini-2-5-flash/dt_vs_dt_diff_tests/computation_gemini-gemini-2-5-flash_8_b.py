
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_day_of_month(dt: datetime) -> datetime:
    # Step 1 & 2: Determine the year and month for the first day of the next month
    if dt.month == 12:
        # If it's December, the next month is January of the next year
        next_month_year = dt.year + 1
        next_month = 1
    else:
        # Otherwise, the next month is simply the current month + 1 in the same year
        next_month_year = dt.year
        next_month = dt.month + 1
    
    # Step 3: Create a datetime object for the first day of the next month
    # We set the day to 1 and the time components to 0 to ensure consistency.
    first_day_of_next_month = datetime(next_month_year, next_month, 1)
    
    # Step 4: Subtract one day to get the last day of the current month
    last_day = first_day_of_next_month - timedelta(days=1)
    
    # Step 5: Return the result as a datetime object
    return last_day

# Entry point: find_last_day_of_month(dt: datetime) -> datetime

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
def test_find_last_day_of_month(dt):
    result = find_last_day_of_month(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

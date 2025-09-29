
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def get_memorial_day_date(year: int) -> datetime:
    # Step 1: Start with the last day of May for the given year.
    # We use 1 for month (May) and 31 for day.
    current_date = datetime(year, 5, 31)

    # Step 2: Iterate backward until a Monday is found.
    # Monday's weekday index is 0.
    while current_date.weekday() != 0:  # 0 represents Monday
        current_date -= timedelta(days=1)
    
    # Step 3: Return the date when the last Monday of May is found.
    return current_date

# Entry point: get_memorial_day_date(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_47_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_get_memorial_day_date(year):
    result = get_memorial_day_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

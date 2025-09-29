
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_memorial_day(year: int) -> date:
    # Step 1: Get the date for May 31st of the given year.
    # This is the latest possible day in May.
    last_day_of_may = date(year, 5, 31)
    
    # Step 2: Calculate the number of days to subtract to get to the preceding or current Monday.
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday.
    # We want to find the Monday (weekday 0).
    # The formula (current_weekday - target_weekday + 7) % 7 gives the number of days
    # to subtract to reach the target_weekday.
    days_to_subtract = (last_day_of_may.weekday() - 0 + 7) % 7
    
    # Step 3: Subtract these days from May 31st to find the last Monday of May.
    memorial_day = last_day_of_may - timedelta(days=days_to_subtract)
    
    # Step 4: Return the calculated date.
    return memorial_day

# Entry point: find_memorial_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_47_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_memorial_day(year):
    result = find_memorial_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

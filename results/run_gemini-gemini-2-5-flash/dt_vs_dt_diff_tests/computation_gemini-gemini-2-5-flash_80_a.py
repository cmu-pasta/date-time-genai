
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_last_weekday_in_month(year: int, month: int, weekday: int) -> date:
    # Step 1: Determine the first day of the next month
    if month == 12:
        # If it's December, the next month is January of the next year
        first_day_of_next_month = date(year + 1, 1, 1)
    else:
        # Otherwise, it's the first day of the next month in the same year
        first_day_of_next_month = date(year, month + 1, 1)
    
    # Step 2: Subtract one day to get the last day of the current month
    last_day_of_current_month = first_day_of_next_month - timedelta(days=1)
    
    # Step 3: Iterate backwards from the last day of the month until the target weekday is found
    current_date = last_day_of_current_month
    while current_date.weekday() != weekday:
        current_date -= timedelta(days=1)
        
    # Step 4: Return the date of the last occurrence of the specific weekday
    return current_date

# Entry point: find_last_weekday_in_month(year: int, month: int, weekday: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_80_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_last_weekday_in_month(year, month, weekday):
    result = find_last_weekday_in_month(year, month, weekday)
    formatted_result = format_value_dt(result, year, month, weekday)
    log_file.write(formatted_result + "\n")

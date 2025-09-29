
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_occurrence_of_weekday(year: int, month: int, target_weekday: int) -> datetime:
    # Step 1: Determine the first day of the month AFTER the target month.
    # This helps in finding the last day of the target month accurately.
    if month == 12:
        # If the target month is December, the next month is January of the next year.
        first_day_of_next_month = datetime(year + 1, 1, 1)
    else:
        # Otherwise, the next month is simply the next chronological month in the same year.
        first_day_of_next_month = datetime(year, month + 1, 1)

    # Step 2: Subtract one day from the first day of the next month to get the last day of the target month.
    current_date = first_day_of_next_month - timedelta(days=1)

    # Step 3: Iterate backward from the last day of the month until the target weekday is found.
    # datetime.weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday.
    while current_date.weekday() != target_weekday:
        current_date = current_date - timedelta(days=1)
    
    # Step 4: Return the datetime object representing the last occurrence of the specific weekday.
    return current_date

# Entry point: find_last_occurrence_of_weekday(year: int, month: int, target_weekday: int) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_80_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_last_occurrence_of_weekday(year, month, target_weekday):
    result = find_last_occurrence_of_weekday(year, month, target_weekday)
    formatted_result = format_value_dt(result, year, month, target_weekday)
    log_file.write(formatted_result + "\n")

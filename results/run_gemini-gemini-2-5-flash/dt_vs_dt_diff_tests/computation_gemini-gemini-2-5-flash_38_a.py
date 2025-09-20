
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_friday_the_13th(start_date: datetime) -> datetime:
    # Step 1: Start checking from the day after the given start_date.
    # This ensures we find an occurrence strictly *after* the input date.
    current_date = start_date + timedelta(days=1)

    # Step 2: Loop indefinitely until a Friday the 13th is found.
    while True:
        # Step 3: Check if the current_date is the 13th day of the month.
        if current_date.day == 13:
            # Step 4: If it's the 13th, check if it's also a Friday.
            # In datetime.weekday(), Monday is 0 and Friday is 4.
            if current_date.weekday() == 4:
                # Step 5: If both conditions are met, this is our target date.
                return current_date
        
        # Step 6: If the current_date is not Friday the 13th,
        # move to the next day and continue the search.
        current_date += timedelta(days=1)

# Entry point: find_next_friday_the_13th(start_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_38_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_friday_the_13th(start_date):
    result = find_next_friday_the_13th(start_date)
    formatted_result = format_value_dt(result, start_date)
    log_file.write(formatted_result + "\n")

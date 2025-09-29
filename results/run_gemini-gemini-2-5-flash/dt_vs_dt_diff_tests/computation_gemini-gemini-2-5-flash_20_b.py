
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_previous_friday(given_date: datetime) -> datetime:
    # Step 1: Get the weekday of the given_date
    # Monday is 0, ..., Friday is 4, ..., Sunday is 6
    current_weekday = given_date.weekday()

    # Step 2: Determine the number of days to subtract to reach the previous Friday
    # If the given_date is a Friday (weekday 4), the previous Friday was 7 days ago.
    if current_weekday == 4:
        days_to_subtract = 7
    # Otherwise, calculate the days difference to the most recent Friday.
    # The formula (current_weekday - target_weekday + 7) % 7 gives days *since* target.
    # Here, target_weekday is 4 (Friday).
    else:
        days_to_subtract = (current_weekday - 4 + 7) % 7
        # If current_weekday is e.g. Monday (0), (0 - 4 + 7) % 7 = 3. Subtract 3 days.
        # If current_weekday is e.g. Saturday (5), (5 - 4 + 7) % 7 = 1. Subtract 1 day.

    # Step 3: Subtract the calculated days from the given_date
    previous_friday = given_date - timedelta(days=days_to_subtract)
    
    # Step 4: Return the resulting datetime object
    return previous_friday

# Entry point: find_previous_friday(given_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_20_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_previous_friday(given_date):
    result = find_previous_friday(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

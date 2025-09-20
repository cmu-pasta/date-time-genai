
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_new_moon(given_date: datetime) -> datetime:
    # Step 1: Define the average synodic month (period between new moons)
    # This is an approximation as the actual period varies slightly.
    synodic_month = timedelta(days=29.530588)

    # Step 2: Establish a known historical new moon date as a reference point.
    # New moon occurred on Jan 6, 2000, at 13:14 UTC.
    reference_new_moon = datetime(2000, 1, 6, 13, 14, 0)

    current_new_moon = reference_new_moon

    # Step 3: Adjust the current_new_moon to be around the given_date.
    # If the given_date is much earlier than our reference, go backward.
    # We aim to get current_new_moon to be the last new moon before or on given_date.
    while current_new_moon > given_date + synodic_month:
        current_new_moon -= synodic_month
    
    # If the given_date is much later than our reference, go forward.
    while current_new_moon <= given_date:
        current_new_moon += synodic_month
    
    # At this point, current_new_moon should be the first new moon *after* given_date.
    return current_new_moon

# Entry point: find_next_new_moon(given_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_74_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_new_moon(given_date):
    result = find_next_new_moon(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

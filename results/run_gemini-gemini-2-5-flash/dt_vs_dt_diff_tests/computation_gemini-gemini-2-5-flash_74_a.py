
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_new_moon(given_date: datetime) -> datetime:
    # Acknowledgment: The datetime library itself does not contain astronomical data
    # or algorithms for calculating moon phases. This solution relies on
    # externally sourced astronomical constants (an epoch new moon date and
    # the average length of a synodic month). These constants are NOT derived
    # from the datetime library but are hardcoded based on astronomical data.
    # Therefore, this implementation strictly adheres to using datetime objects
    # and operations, but the core astronomical knowledge is external to the library.

    # Step 1: Define a known new moon epoch (e.g., a new moon around 2000-01-01)
    # This specific date (2000-01-06) is an actual new moon date.
    new_moon_epoch = datetime(2000, 1, 6, 13, 14, 0) # January 6, 2000, 13:14 UTC

    # Step 2: Define the average length of a synodic month (lunar cycle)
    # Approximately 29.530588 days.
    synodic_month_timedelta = timedelta(days=29.530588)

    # Step 3: Start from the epoch and advance until we find a new moon after the given_date
    current_new_moon = new_moon_epoch

    # Adjust the initial current_new_moon to be somewhat close to the given_date
    # without iterating too many times from 2000-01-06 for very future dates.
    # We can calculate how many synodic months have passed since the epoch.
    if given_date > new_moon_epoch:
        difference = given_date - new_moon_epoch
        num_months = int(difference.total_seconds() / synodic_month_timedelta.total_seconds())
        current_new_moon = new_moon_epoch + num_months * synodic_month_timedelta

    # Now, iterate forward from a point near or before the given_date
    while current_new_moon <= given_date:
        current_new_moon += synodic_month_timedelta
    
    # Step 4: Return the first new moon date found that is after the given_date
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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_74_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_new_moon(given_date):
    result = find_next_new_moon(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

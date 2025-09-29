
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_full_moon(reference_date: datetime) -> datetime:
    # IMPORTANT NOTE: This function provides an APPROXIMATE calculation of the next full moon.
    # The datetime library itself does not contain astronomical calculation capabilities.
    # This approximation relies on an average synodic month length and a hardcoded
    # known full moon date. For accurate results, a dedicated astronomical library
    # (e.g., PyEphem, astropy) would be required.

    # Step 1: Establish known constants. These are external to the datetime library.
    # Using a known full moon date as a starting point (e.g., October 28, 2023, 08:24 UTC)
    # Source for reference date: Time and Date (https://www.timeanddate.com/moon/phases/)
    # For simplicity, we'll use a local timezone or assume UTC and handle timezone-naiveness.
    # Let's use a naive datetime for the reference.
    KNOWN_FULL_MOON_EPOCH = datetime(2023, 10, 28, 8, 24)
    
    # Average length of a synodic month (time between two successive full moons)
    # Approximately 29.530588 days
    # Converted to a timedelta object for arithmetic
    AVERAGE_SYNODIC_MONTH = timedelta(days=29.530588)

    # Step 2: Calculate the difference in days from the epoch to the reference_date
    # This helps in finding an initial estimate for the iteration.
    diff_from_epoch = reference_date - KNOWN_FULL_MOON_EPOCH
    
    # Step 3: Estimate how many full moons have passed since the epoch relative to reference_date
    # We add a buffer of 2 months to ensure we start before the reference_date.
    num_months_estimate = int(diff_from_epoch.days / AVERAGE_SYNODIC_MONTH.days) - 2
    
    # Step 4: Start from an estimated full moon date and iterate forward
    # Ensure the initial candidate is well before the reference_date to catch the first one
    current_full_moon_candidate = KNOWN_FULL_MOON_EPOCH + (num_months_estimate * AVERAGE_SYNODIC_MONTH)
    
    # Iterate until we find the first full moon date after the reference_date
    while current_full_moon_candidate <= reference_date:
        current_full_moon_candidate += AVERAGE_SYNODIC_MONTH
        
    # Step 5: Return the result
    return current_full_moon_candidate

# Entry point: find_next_full_moon(reference_date: datetime) -> datetime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_23_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_full_moon(reference_date):
    result = find_next_full_moon(reference_date)
    formatted_result = format_value_dt(result, reference_date)
    log_file.write(formatted_result + "\n")

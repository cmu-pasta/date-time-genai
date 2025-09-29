
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_full_moon(start_date: datetime) -> datetime:
    # Step 1: Define a known reference full moon date and the average synodic period.
    # These values are empirical and are not calculated by the datetime library itself.
    # The datetime library is used here to represent and manipulate these external values.
    REFERENCE_FULL_MOON = datetime(2023, 10, 28, 20, 24, 0) # Full Moon on Oct 28, 2023 8:24 PM UTC
    MOON_CYCLE_DAYS = 29.530588 # Average synodic period of the moon in days

    # Step 2: Convert the moon cycle days into a timedelta for calculations
    moon_cycle_timedelta = timedelta(days=MOON_CYCLE_DAYS)

    # Step 3: Ensure the start_date is naive if REFERENCE_FULL_MOON is naive, for consistent comparison
    # Or, if zones are involved, ensure both are in the same zone. For simplicity, we assume naive datetimes.
    # Let's consider the input date's time component if it's earlier than the reference,
    # or just use the date part to simplify. The problem asks for the date, but full moon
    # events have a specific time. We will return the datetime of the event.
    
    # Step 4: Calculate the difference between the start date and the reference full moon
    # We use the reference as a base. We need to find the number of cycles after the reference.
    
    # If the start_date is before or on the reference full moon, we might start counting from an earlier
    # reference or ensure our first calculated full moon is after start_date.
    
    # Calculate how many full moon cycles have passed since the reference to reach around the start_date
    delta_to_start = start_date - REFERENCE_FULL_MOON
    
    # Calculate the number of full moon cycles that have occurred. Use floor division for integer cycles.
    # We want to find the *next* full moon *after* start_date.
    # If delta_to_start is positive, this gives cycles after reference.
    # If delta_to_start is negative, this gives cycles before reference.
    num_cycles_approx = delta_to_start.total_seconds() / moon_cycle_timedelta.total_seconds()
    
    # The number of cycles to add to REFERENCE_FULL_MOON to get to the first full moon
    # that is *on or after* the start_date.
    
    # If num_cycles_approx is an exact integer, and REFERENCE_FULL_MOON + num_cycles_approx * moon_cycle_timedelta
    # is exactly start_date, then we need the *next* one, so we add 1.
    # Otherwise, we floor it and add 1 to ensure it's truly the *next* one.
    
    # We want the smallest 'n' such that REFERENCE_FULL_MOON + n * MOON_CYCLE_DAYS >= start_date
    # n >= (start_date - REFERENCE_FULL_MOON) / MOON_CYCLE_DAYS
    # n = ceil((start_date - REFERENCE_FULL_MOON) / MOON_CYCLE_DAYS)
    
    # Calculate initial estimate for full moon:
    estimated_full_moon = REFERENCE_FULL_MOON
    
    # Adjust until it's past the start_date
    while estimated_full_moon <= start_date:
        estimated_full_moon += moon_cycle_timedelta
            
    return estimated_full_moon

# Entry point: find_next_full_moon(start_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_23_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_full_moon(start_date):
    result = find_next_full_moon(start_date)
    formatted_result = format_value_dt(result, start_date)
    log_file.write(formatted_result + "\n")

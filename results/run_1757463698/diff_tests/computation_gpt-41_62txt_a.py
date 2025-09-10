
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def full_moons_between(start_date: date, end_date: date) -> int:
    # Step 1: Define a known full moon reference date.
    reference_full_moon = date(2000, 1, 21)  # January 21, 2000 was a full moon
    
    # Step 2: Synodic month duration (average full moon cycle)
    synodic_month = 29.530588853  # days (from astronomical data)
    
    # Step 3: Sort the input dates so start_date <= end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Step 4: Calculate number of full moons since reference for both dates.
    days_from_reference_start = (start_date - reference_full_moon).days
    days_from_reference_end   = (end_date - reference_full_moon).days
    
    cycles_start = days_from_reference_start / synodic_month
    cycles_end   = days_from_reference_end   / synodic_month
    
    # Step 5: Calculate the number of full moons between the two dates.
    # Use floor for the starting position and for the ending position.
    full_moons = int(cycles_end // 1) - int(cycles_start // 1)
    
    return full_moons

# Entry point: full_moons_between(start_date: date, end_date: date) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_62txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_full_moons_between(start_date, end_date):
    result = full_moons_between(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")

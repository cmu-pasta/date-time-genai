
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_full_moon(given_date: datetime) -> datetime:
    # Known full moon reference date: January 17, 2022 at 23:48 UTC
    reference_full_moon = datetime(2022, 1, 17, 23, 48)
    
    # Average lunar cycle length in days
    lunar_cycle_days = 29.530588853
    
    # Calculate the number of days between given date and reference
    days_difference = (given_date - reference_full_moon).total_seconds() / (24 * 3600)
    
    # Calculate how many complete lunar cycles have passed
    cycles_passed = days_difference / lunar_cycle_days
    
    # Find the next full moon cycle number
    if given_date <= reference_full_moon:
        # If given date is before or equal to reference, use reference date
        next_cycle = 0
    else:
        # If given date is after reference, find the next cycle
        next_cycle = int(cycles_passed) + 1
    
    # Calculate the next full moon date
    days_to_add = next_cycle * lunar_cycle_days
    next_full_moon = reference_full_moon + timedelta(days=days_to_add)
    
    # Ensure the calculated date is actually after the given date
    while next_full_moon <= given_date:
        next_full_moon += timedelta(days=lunar_cycle_days)
    
    return next_full_moon

# Entry point: find_next_full_moon(given_date: datetime) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_23_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_full_moon(given_date):
    result = find_next_full_moon(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_full_moon(given_date: datetime) -> datetime:
    # Reference full moon date: January 17, 2022
    reference_full_moon = datetime(2022, 1, 17)
    
    # Average lunar cycle length in days
    lunar_cycle_days = 29.53059
    
    # Calculate days difference from reference to given date
    days_diff = (given_date - reference_full_moon).days
    
    # Calculate how many complete lunar cycles have passed
    cycles_passed = days_diff // lunar_cycle_days
    
    # Calculate the most recent full moon before or on the given date
    recent_full_moon_days = cycles_passed * lunar_cycle_days
    recent_full_moon = reference_full_moon + timedelta(days=recent_full_moon_days)
    
    # If the recent full moon is after the given date, we need the previous one
    if recent_full_moon > given_date:
        recent_full_moon = recent_full_moon - timedelta(days=lunar_cycle_days)
    
    # Calculate the next full moon after the given date
    next_full_moon = recent_full_moon + timedelta(days=lunar_cycle_days)
    
    # Ensure the result is after the given date
    while next_full_moon <= given_date:
        next_full_moon = next_full_moon + timedelta(days=lunar_cycle_days)
    
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_23_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_full_moon(given_date):
    result = find_next_full_moon(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

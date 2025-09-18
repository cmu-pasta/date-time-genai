
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def next_full_moon(given_date: datetime) -> datetime:
    # Reference full moon date: January 6, 2000
    reference_full_moon = datetime(2000, 1, 6, 18, 14)  # Approximate time of full moon
    
    # Average lunar cycle length in days
    lunar_cycle_days = 29.53058867
    
    # Calculate days since reference full moon
    days_since_reference = (given_date - reference_full_moon).total_seconds() / (24 * 3600)
    
    # Calculate number of complete cycles since reference
    cycles_since_reference = int(days_since_reference / lunar_cycle_days)
    
    # Calculate the most recent full moon
    recent_full_moon = reference_full_moon + timedelta(days=cycles_since_reference * lunar_cycle_days)
    
    # If the recent full moon is after the given date, return it
    # Otherwise, calculate the next full moon
    if recent_full_moon > given_date:
        next_moon = recent_full_moon
    else:
        next_moon = reference_full_moon + timedelta(days=(cycles_since_reference + 1) * lunar_cycle_days)
    
    return next_moon

# Entry point: next_full_moon(given_date: datetime) -> datetime

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_23txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_full_moon(given_date):
    result = next_full_moon(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

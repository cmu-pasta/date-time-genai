
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_new_moon(given_date: datetime) -> datetime:
    # Reference new moon date: January 6, 2000
    reference_new_moon = datetime(2000, 1, 6)
    
    # Average length of a lunar month in days
    lunar_cycle_days = 29.53059
    
    # Calculate the number of days since the reference new moon
    days_since_reference = (given_date - reference_new_moon).total_seconds() / (24 * 3600)
    
    # Calculate the number of complete lunar cycles since reference
    cycles_passed = int(days_since_reference / lunar_cycle_days)
    
    # Calculate the date of the most recent new moon before or on the given date
    recent_new_moon = reference_new_moon + timedelta(days=cycles_passed * lunar_cycle_days)
    
    # If the recent new moon is before the given date, get the next one
    if recent_new_moon <= given_date:
        next_new_moon = recent_new_moon + timedelta(days=lunar_cycle_days)
    else:
        next_new_moon = recent_new_moon
    
    return next_new_moon

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_74txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_new_moon(given_date):
    result = find_next_new_moon(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

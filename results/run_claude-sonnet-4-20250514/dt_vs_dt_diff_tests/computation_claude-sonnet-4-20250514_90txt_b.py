
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_lunar_age(given_date: datetime) -> int:
    # Reference new moon: January 6, 2000, 18:14 UTC
    # This is a well-documented new moon used in astronomical calculations
    reference_new_moon = datetime(2000, 1, 6, 18, 14)
    
    # Average lunar cycle length in days (synodic month)
    lunar_cycle_days = 29.53059
    
    # Calculate the difference in days between given date and reference
    days_since_reference = (given_date - reference_new_moon).total_seconds() / (24 * 3600)
    
    # Calculate lunar age using modulo operation
    # This gives us days since the most recent new moon
    lunar_age = days_since_reference % lunar_cycle_days
    
    # Return as integer (rounded down)
    return int(lunar_age)

# Entry point: calculate_lunar_age(given_date: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_90txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_lunar_age(given_date):
    result = calculate_lunar_age(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

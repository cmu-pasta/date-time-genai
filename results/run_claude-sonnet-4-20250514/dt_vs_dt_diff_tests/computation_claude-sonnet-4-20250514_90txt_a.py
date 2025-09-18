
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_lunar_age(date: datetime) -> float:
    # Reference new moon: January 1, 2000, 18:14 UTC
    reference_new_moon = datetime(2000, 1, 1, 18, 14, 0)
    
    # Lunar cycle length in days (synodic month)
    lunar_cycle_days = 29.530588853
    
    # Calculate the difference in days between the given date and reference
    time_difference = date - reference_new_moon
    days_difference = time_difference.total_seconds() / (24 * 60 * 60)
    
    # Calculate lunar age using modulo operation
    lunar_age = days_difference % lunar_cycle_days
    
    # Ensure the result is positive
    if lunar_age < 0:
        lunar_age += lunar_cycle_days
    
    return lunar_age

# Entry point: calculate_lunar_age(date: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_90txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_lunar_age(date):
    result = calculate_lunar_age(date)
    formatted_result = format_value_dt(result, date)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_new_moon(given_date: datetime) -> datetime:
    # Reference new moon date: January 6, 2000, 18:14 UTC (approximately)
    reference_new_moon = datetime(2000, 1, 6, 18, 14, 0)
    
    # Average synodic month length in days
    synodic_month_days = 29.53059
    
    # Calculate days difference from reference date
    days_diff = (given_date - reference_new_moon).total_seconds() / (24 * 3600)
    
    # Calculate number of synodic months since reference
    months_since_ref = days_diff / synodic_month_days
    
    # Find the next integer number of months
    next_month_count = int(months_since_ref) + 1
    
    # Calculate the next new moon date
    next_new_moon = reference_new_moon + timedelta(days=next_month_count * synodic_month_days)
    
    # If the calculated date is still before or equal to the given date, add one more month
    if next_new_moon <= given_date:
        next_new_moon = reference_new_moon + timedelta(days=(next_month_count + 1) * synodic_month_days)
    
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_74_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_new_moon(given_date):
    result = find_next_new_moon(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")

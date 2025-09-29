
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def calculate_lunar_age(dt: datetime) -> float:
    # Step 1: Reference new moon (UTC): 2000-01-06 18:14 UTC
    reference_new_moon = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Step 2: Synodic month length in days (mean lunar cycle)
    synodic_month_days = 29.530588853
    
    # Step 3: Normalize input datetime to UTC
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)
    
    # Step 4: Compute elapsed time since reference new moon
    elapsed = dt_utc - reference_new_moon
    
    # Step 5: Convert elapsed time to days (float)
    elapsed_days = elapsed.total_seconds() / 86400.0
    
    # Step 6: Compute lunar age modulo the synodic month
    lunar_age_days = elapsed_days % synodic_month_days
    
    # Step 7: Return lunar age in days as a float
    return float(lunar_age_days)

# Entry point: calculate_lunar_age(dt: datetime) -> float

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_90_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_lunar_age(dt):
    result = calculate_lunar_age(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
def next_new_moon(after_dt: datetime) -> datetime:
    # Average synodic month (new moon to new moon) in days
    synodic_days = 29.530588853
    
    # Reference new moon (UTC): 2000-01-06 18:14:00 UTC
    epoch = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    
    # Normalize input to UTC: assume UTC if naive
    if after_dt.tzinfo is None:
        base = after_dt.replace(tzinfo=timezone.utc)
    else:
        base = after_dt.astimezone(timezone.utc)
    
    # Elapsed days since epoch
    delta_days = (base - epoch).total_seconds() / 86400.0
    
    # Integer cycle index not exceeding the elapsed time
    k = int(delta_days / synodic_days)
    
    # Candidate new moon at cycle k
    candidate = epoch + timedelta(days=synodic_days * k)
    
    # Ensure the result is strictly after the given datetime
    if candidate <= base:
        k += 1
        candidate = epoch + timedelta(days=synodic_days * k)
    
    return candidate

# Entry point: next_new_moon(after_dt: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_74_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_new_moon(after_dt):
    result = next_new_moon(after_dt)
    formatted_result = format_value_dt(result, after_dt)
    log_file.write(formatted_result + "\n")

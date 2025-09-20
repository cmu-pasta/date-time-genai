
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
def next_full_moon(after: datetime) -> datetime:
    # Step 1: Known full moon reference (NASA): 2000-01-21 16:41 UTC
    epoch_naive = datetime(2000, 1, 21, 16, 41)
    epoch_utc = datetime(2000, 1, 21, 16, 41, tzinfo=timezone.utc)
    
    # Step 2: Synodic month length (mean time between full moons)
    synodic_period = timedelta(days=29.530588853)
    
    # Step 3: Match epoch's timezone-awareness to input
    if after.tzinfo is None or after.tzinfo.utcoffset(after) is None:
        epoch = epoch_naive
    else:
        epoch = epoch_utc.astimezone(after.tzinfo)
    
    # Step 4: Compute elapsed periods (use truncation toward zero, then adjust)
    elapsed = (after - epoch) / synodic_period  # float
    base_n = int(elapsed)  # truncates toward zero
    
    # Step 5: Build candidate and advance until strictly after input
    candidate = epoch + synodic_period * base_n
    while candidate <= after:
        candidate = candidate + synodic_period
    
    return candidate

# Entry point: next_full_moon(after: datetime) -> datetime

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_23_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_full_moon(after):
    result = next_full_moon(after)
    formatted_result = format_value_dt(result, after)
    log_file.write(formatted_result + "\n")

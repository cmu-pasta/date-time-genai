
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time, timedelta
def minutes_between(t1: time, t2: time) -> int:
    # Step 1: Use a fixed common date to ensure both times are on the same day
    common_date = date(2000, 1, 1)
    dt1 = datetime.combine(common_date, t1)
    dt2 = datetime.combine(common_date, t2)
    
    # Step 2: Compute the difference and convert to absolute minutes
    delta = abs(dt2 - dt1)
    minutes = delta // timedelta(minutes=1)  # Floor division to get integer minutes
    
    # Step 3: Return the integer number of minutes
    return int(minutes)

# Entry point: minutes_between(t1: time, t2: time) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_33_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_minutes_between(t1, t2):
    result = minutes_between(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, time, datetime
def minutes_between_same_day(d: date, t1: time, t2: time) -> int:
    # Combine the given date with each time to create datetime objects on the same day
    dt1 = datetime.combine(d, t1)
    dt2 = datetime.combine(d, t2)
    
    # Compute the difference as a timedelta
    delta = dt2 - dt1
    
    # Convert the difference to a non-negative integer number of minutes
    minutes = int(abs(delta.total_seconds()) // 60)
    return minutes

# Entry point: minutes_between_same_day(d: date, t1: time, t2: time) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_33_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), time_strategy(), time_strategy())
def test_minutes_between_same_day(d, t1, t2):
    result = minutes_between_same_day(d, t1, t2)
    formatted_result = format_value_dt(result, d, t1, t2)
    log_file.write(formatted_result + "\n")

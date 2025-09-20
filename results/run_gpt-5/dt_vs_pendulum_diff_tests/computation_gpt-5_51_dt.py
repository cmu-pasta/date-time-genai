
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time, timedelta
def calculate_total_minutes_between_times(t1: time, t2: time) -> int:
    # Anchor both times to the same arbitrary date
    base_date = datetime(2000, 1, 1)
    start_dt = datetime.combine(base_date.date(), t1)
    end_dt = datetime.combine(base_date.date(), t2)
    
    # Handle crossing midnight: if end is earlier than start, add 1 day to end
    if end_dt < start_dt:
        end_dt += timedelta(days=1)
    
    # Calculate the difference and convert to total minutes
    delta = end_dt - start_dt
    total_minutes = int(delta.total_seconds() // 60)
    return total_minutes

# Entry point: calculate_total_minutes_between_times(t1: time, t2: time) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_51_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_total_minutes_between_times(t1, t2):
    result = calculate_total_minutes_between_times(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")

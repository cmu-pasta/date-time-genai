
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time
def calculate_time_difference_hours(t1: time, t2: time) -> float:
    # Step 1: Combine times with the same arbitrary date to create datetime objects
    base_day = date(2000, 1, 1)
    dt1 = datetime.combine(base_day, t1)
    dt2 = datetime.combine(base_day, t2)
    
    # Step 2: Compute the absolute difference within the same day
    delta_seconds = abs((dt2 - dt1).total_seconds())
    
    # Step 3: Convert seconds to hours and return
    hours = delta_seconds / 3600.0
    return hours

# Entry point: calculate_time_difference_hours(t1: time, t2: time) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_18_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_time_difference_hours(t1, t2):
    result = calculate_time_difference_hours(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")

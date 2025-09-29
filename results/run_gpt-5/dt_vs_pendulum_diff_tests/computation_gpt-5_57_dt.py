
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_work_weeks_between(d1: date, d2: date) -> int:
    # Step 1: Normalize the date order to ensure start <= end
    if d1 <= d2:
        start = d1
        end = d2
    else:
        start = d2
        end = d1

    # Step 2: Compute total days in the half-open interval [start, end)
    total_days = (end - start).days  # exclusive of the end date

    # Step 3: Convert total days to business days (weekdays only)
    full_weeks = total_days // 7
    remainder = total_days % 7
    start_weekday = start.weekday()  # Monday=0 ... Sunday=6

    business_days = full_weeks * 5
    for i in range(remainder):
        if (start_weekday + i) % 7 < 5:  # Monday-Friday are < 5
            business_days += 1

    # Step 4: Convert business days to complete work weeks
    work_weeks = business_days // 5
    return work_weeks

# Entry point: calculate_work_weeks_between(d1: date, d2: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_57_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_work_weeks_between(d1, d2):
    result = calculate_work_weeks_between(d1, d2)
    formatted_result = format_value_dt(result, d1, d2)
    log_file.write(formatted_result + "\n")

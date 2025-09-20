
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_weekend_days_between(d1: date, d2: date) -> int:
    # Step 1: Normalize date order
    start = d1 if d1 <= d2 else d2
    end = d2 if d2 >= d1 else d1

    # Step 2: Compute total days inclusive
    total_days_inclusive = (end - start).days + 1

    # Step 3: Weekend days from full weeks
    full_weeks = total_days_inclusive // 7
    weekend_days = full_weeks * 2  # Saturday and Sunday per full week

    # Step 4: Count weekend days in the remaining partial week
    remainder_days = total_days_inclusive % 7
    start_wd = start.weekday()  # Monday=0 ... Sunday=6
    extra_weekend_days = 0
    for i in range(remainder_days):
        wd = (start_wd + i) % 7
        if wd >= 5:  # 5=Saturday, 6=Sunday
            extra_weekend_days += 1

    # Step 5: Total weekend days
    return weekend_days + extra_weekend_days

# Entry point: calculate_weekend_days_between(d1: date, d2: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_15_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_weekend_days_between(d1, d2):
    result = calculate_weekend_days_between(d1, d2)
    formatted_result = format_value_dt(result, d1, d2)
    log_file.write(formatted_result + "\n")

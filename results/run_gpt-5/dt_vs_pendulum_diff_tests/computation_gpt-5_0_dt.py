
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_business_days(d1: date, d2: date) -> int:
    """
    Calculate the number of business days (Monday-Friday) between two dates, inclusive.
    Inputs: d1 (date), d2 (date)
    Output: int (number of business days)
    """
    # Ensure d1 <= d2 by swapping if necessary
    if d1 > d2:
        d1, d2 = d2, d1

    # Inclusive total days between dates
    total_days = (d2 - d1).days + 1

    # Business days contributed by full weeks
    full_weeks = total_days // 7
    business_days = full_weeks * 5

    # Remaining days after full weeks
    remainder = total_days % 7
    start_weekday = d1.weekday()  # 0=Monday, 6=Sunday

    # Count weekdays in the remainder span
    for i in range(remainder):
        if (start_weekday + i) % 7 < 5:
            business_days += 1

    return business_days

# Entry point: calculate_business_days(d1: date, d2: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_0_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_business_days(d1, d2):
    result = calculate_business_days(d1, d2)
    formatted_result = format_value_dt(result, d1, d2)
    log_file.write(formatted_result + "\n")

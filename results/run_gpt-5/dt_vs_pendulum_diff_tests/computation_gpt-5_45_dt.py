
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def business_days_remaining_in_month(d: date) -> int:
    """
    Calculate the number of business days (Mon-Fri) remaining in the month,
    including the given date if it is a business day.
    """
    # Determine the first day of the next month
    if d.month == 12:
        next_month_first = date(d.year + 1, 1, 1)
    else:
        next_month_first = date(d.year, d.month + 1, 1)
    
    # Last day of the current month
    last_day = next_month_first - timedelta(days=1)
    
    # Count business days from d through last_day (inclusive)
    count = 0
    current = d
    one_day = timedelta(days=1)
    while current <= last_day:
        # Monday=0 ... Sunday=6; business days are 0..4
        if current.weekday() < 5:
            count += 1
        current += one_day
    
    return count

# Entry point: business_days_remaining_in_month(d: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_45_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_business_days_remaining_in_month(d):
    result = business_days_remaining_in_month(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")

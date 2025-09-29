
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_business_days_remaining(current_date: date) -> int:
    # Step 1: Determine the first day of the next month
    if current_date.month == 12:
        next_month_first = date(current_date.year + 1, 1, 1)
    else:
        next_month_first = date(current_date.year, current_date.month + 1, 1)
    
    # Step 2: Determine the last day of the current month
    last_day_of_month = next_month_first - timedelta(days=1)
    
    # Step 3: Count business days (Monday=0 to Friday=4) from current_date to end of month inclusive
    count = 0
    day = current_date
    one_day = timedelta(days=1)
    while day <= last_day_of_month:
        if day.weekday() < 5:
            count += 1
        day += one_day
    
    # Step 4: Return the total number of business days remaining
    return count

# Entry point: calculate_business_days_remaining(current_date: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_45_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_business_days_remaining(current_date):
    result = calculate_business_days_remaining(current_date)
    formatted_result = format_value_dt(result, current_date)
    log_file.write(formatted_result + "\n")

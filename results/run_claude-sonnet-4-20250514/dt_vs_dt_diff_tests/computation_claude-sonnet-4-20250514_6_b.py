
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_age_in_days(birth_date: datetime, current_date: datetime) -> int:
    # Ensure current_date is after birth_date for positive age
    if current_date < birth_date:
        birth_date, current_date = current_date, birth_date
    
    # Calculate the difference in days
    age_in_days = (current_date - birth_date).days
    
    return age_in_days

# Entry point: calculate_age_in_days(birth_date: datetime, current_date: datetime) -> int

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_6_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_age_in_days(birth_date, current_date):
    result = calculate_age_in_days(birth_date, current_date)
    formatted_result = format_value_dt(result, birth_date, current_date)
    log_file.write(formatted_result + "\n")

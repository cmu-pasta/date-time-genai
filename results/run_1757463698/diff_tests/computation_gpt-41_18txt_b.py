
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_weeks_difference(date1: date, date2: date) -> int:
    # Step 1: Calculate the difference in days
    days_difference = abs((date2 - date1).days)
    
    # Step 2: Calculate the number of complete weeks (integer division)
    weeks_difference = days_difference // 7
    
    # Step 3: Return the number of weeks as an integer
    return weeks_difference

# Entry point: calculate_weeks_difference(date1: date, date2: date) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_18txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_weeks_difference(date1, date2):
    result = calculate_weeks_difference(date1, date2)
    formatted_result = format_value_dt(result, date1, date2)
    log_file.write(formatted_result + "\n")

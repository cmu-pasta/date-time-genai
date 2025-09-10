
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def get_week_start_sunday(input_date: date) -> date:
    # Step 1: Determine the weekday index (Monday=0, Sunday=6)
    weekday_index = input_date.weekday()
    # Step 2: Calculate the number of days to subtract to reach the previous Sunday
    days_to_subtract = (weekday_index + 1) % 7
    # Step 3: Compute and return the week's start date (Sunday)
    week_start_date = input_date - timedelta(days=days_to_subtract)
    return week_start_date

# Entry point: get_week_start_sunday(input_date: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_38txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_get_week_start_sunday(input_date):
    result = get_week_start_sunday(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")

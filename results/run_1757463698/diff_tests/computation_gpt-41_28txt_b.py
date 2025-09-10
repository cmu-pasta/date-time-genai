
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def roll_forward_to_next_month_start(dt: date) -> date:
    # Step 1: Check if current month is December
    if dt.month == 12:
        # Next month is January of the next year
        next_month = 1
        next_year = dt.year + 1
    else:
        # Normal case: increment the month
        next_month = dt.month + 1
        next_year = dt.year
    # Step 2: Construct and return the first day of the next month
    return date(next_year, next_month, 1)

# Entry point: roll_forward_to_next_month_start(dt: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_28txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_roll_forward_to_next_month_start(dt):
    result = roll_forward_to_next_month_start(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

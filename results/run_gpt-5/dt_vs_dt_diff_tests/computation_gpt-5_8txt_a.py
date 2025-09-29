
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def last_day_of_month(d: date) -> date:
    # Step 1: Determine the first day of the next month
    if d.month == 12:
        first_of_next_month = date(d.year + 1, 1, 1)
    else:
        first_of_next_month = date(d.year, d.month + 1, 1)
    
    # Step 2: Subtract one day to get the last day of the current month
    last_day = first_of_next_month - timedelta(days=1)
    
    # Step 3: Return the last day of the month
    return last_day

# Entry point: last_day_of_month(d: date) -> date

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_8txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_last_day_of_month(d):
    result = last_day_of_month(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")

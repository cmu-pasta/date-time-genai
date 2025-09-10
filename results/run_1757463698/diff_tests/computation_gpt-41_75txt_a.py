
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def start_of_next_quarter(dt: datetime) -> datetime:
    # Step 1: Identify the current quarter (1, 2, 3, or 4)
    current_month = dt.month
    # Quarters start at months 1, 4, 7, 10
    current_quarter = ((current_month - 1) // 3) + 1
    
    # Step 2: Compute the start month of the next quarter
    if current_quarter < 4:
        next_quarter_month = 1 + current_quarter * 3
        next_quarter_year = dt.year
    else:  # current_quarter == 4
        next_quarter_month = 1
        next_quarter_year = dt.year + 1

    # Step 3: Return the corresponding datetime, set to the first day at midnight
    return datetime(
        year=next_quarter_year,
        month=next_quarter_month,
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=dt.tzinfo
    )

# Entry point: start_of_next_quarter(dt: datetime) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_75txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_start_of_next_quarter(dt):
    result = start_of_next_quarter(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

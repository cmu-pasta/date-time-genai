
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def start_of_next_quarter(dt: datetime) -> datetime:
    # Step 1: Determine the start month of the next quarter
    month = dt.month
    year = dt.year

    # Quarters: (start_months: 1, 4, 7, 10)
    if month <= 3:
        next_q_month = 4
        next_q_year = year
    elif month <= 6:
        next_q_month = 7
        next_q_year = year
    elif month <= 9:
        next_q_month = 10
        next_q_year = year
    else:  # month 10-12
        next_q_month = 1
        next_q_year = year + 1

    # Step 2: Construct the datetime at the start of the next quarter (00:00:00)
    next_quarter_start = datetime(next_q_year, next_q_month, 1, 0, 0, 0, tzinfo=dt.tzinfo)

    return next_quarter_start

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_75txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_start_of_next_quarter(dt):
    result = start_of_next_quarter(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

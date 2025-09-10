
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def days_left_in_quarter(dt: date) -> int:
    # Step 3: Determine which quarter the date belongs to
    year = dt.year
    if dt.month <= 3:
        # Q1: Jan 1 - Mar 31
        last_day_of_quarter = date(year, 3, 31)
    elif dt.month <= 6:
        # Q2: Apr 1 - Jun 30
        last_day_of_quarter = date(year, 6, 30)
    elif dt.month <= 9:
        # Q3: Jul 1 - Sep 30
        last_day_of_quarter = date(year, 9, 30)
    else:
        # Q4: Oct 1 - Dec 31
        last_day_of_quarter = date(year, 12, 31)
    
    # Step 5: Compute the difference
    days_left = (last_day_of_quarter - dt).days + 1  # +1 to include the end date
    
    # If the date is already past the last day of the quarter (shouldn't happen), return 0
    return max(0, days_left)

# Entry point: days_left_in_quarter(dt: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_29txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_days_left_in_quarter(dt):
    result = days_left_in_quarter(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

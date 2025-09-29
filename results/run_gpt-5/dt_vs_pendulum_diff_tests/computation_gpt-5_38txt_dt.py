
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def next_friday_the_13th(after_date: date) -> date:
    """
    Find the next occurrence of Friday the 13th strictly after the given date.
    
    Parameters:
    - after_date: date
    
    Returns:
    - date of the next Friday the 13th strictly after 'after_date'
    """
    # Step 1: Start from the day strictly after the given date
    start = after_date + timedelta(days=1)
    
    # Step 2: Determine the first candidate 13th on or after 'start'
    year = start.year
    month = start.month
    if start.day <= 13:
        candidate = date(year, month, 13)
    else:
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        candidate = date(year, month, 13)
    
    # Step 3: Iterate month-by-month until the 13th is a Friday (weekday() == 4)
    while candidate.weekday() != 4:  # Monday=0, ..., Friday=4
        if candidate.month == 12:
            year = candidate.year + 1
            month = 1
        else:
            year = candidate.year
            month = candidate.month + 1
        candidate = date(year, month, 13)
    
    # Step 4: Return the found date
    return candidate

# Entry point: next_friday_the_13th(after_date: date) -> date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_38txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_friday_the_13th(after_date):
    result = next_friday_the_13th(after_date)
    formatted_result = format_value_dt(result, after_date)
    log_file.write(formatted_result + "\n")

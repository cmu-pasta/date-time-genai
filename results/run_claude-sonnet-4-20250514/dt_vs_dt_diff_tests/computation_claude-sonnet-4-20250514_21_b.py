
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def days_until_next_birthday(birth_date: datetime) -> int:
    # Get current date and time
    now = datetime.now()
    
    # Create this year's birthday with the same month and day as birth_date
    this_year_birthday = datetime(now.year, birth_date.month, birth_date.day)
    
    # If birthday already passed this year, use next year
    if this_year_birthday < now:
        next_birthday = datetime(now.year + 1, birth_date.month, birth_date.day)
    else:
        next_birthday = this_year_birthday
    
    # Calculate difference in days
    days_until = (next_birthday - now).days
    
    return days_until

# Entry point: days_until_next_birthday(birth_date: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_21_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_days_until_next_birthday(birth_date):
    result = days_until_next_birthday(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")

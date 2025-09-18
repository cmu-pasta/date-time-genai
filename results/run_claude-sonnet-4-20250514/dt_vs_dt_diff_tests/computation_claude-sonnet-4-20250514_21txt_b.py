
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def days_until_next_birthday(birth_date: date) -> int:
    # Step 1: Get today's date
    today = date.today()
    
    # Step 2: Create this year's birthday date
    current_year = today.year
    this_year_birthday = date(current_year, birth_date.month, birth_date.day)
    
    # Step 3: Check if this year's birthday has already passed
    if this_year_birthday < today:
        # Birthday has passed, calculate days until next year's birthday
        next_year_birthday = date(current_year + 1, birth_date.month, birth_date.day)
        days_until = (next_year_birthday - today).days
    elif this_year_birthday > today:
        # Birthday hasn't occurred yet this year
        days_until = (this_year_birthday - today).days
    else:
        # Today is the birthday!
        days_until = 0
    
    # Step 4: Return the result as an integer
    return days_until

# Entry point: days_until_next_birthday(birth_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_21txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_days_until_next_birthday(birth_date):
    result = days_until_next_birthday(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")

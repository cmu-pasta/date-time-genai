
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def days_until_next_birthday(birth_date: date) -> int:
    today = date.today()
    
    try:
        # Create this year's birthday
        this_year_birthday = date(today.year, birth_date.month, birth_date.day)
    except ValueError:
        # Handle leap year case (Feb 29 in non-leap year) - use Feb 28
        this_year_birthday = date(today.year, 2, 28)
    
    # If this year's birthday has already passed, calculate for next year
    if this_year_birthday < today:
        try:
            next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
        except ValueError:
            # Handle leap year case for next year
            next_birthday = date(today.year + 1, 2, 28)
    else:
        next_birthday = this_year_birthday
    
    # Calculate the difference in days
    days_until = (next_birthday - today).days
    
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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_21txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_days_until_next_birthday(birth_date):
    result = days_until_next_birthday(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")

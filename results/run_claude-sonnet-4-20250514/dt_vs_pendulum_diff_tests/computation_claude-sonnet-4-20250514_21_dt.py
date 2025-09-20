
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_days_until_next_birthday(birth_date: datetime) -> int:
    # Get current date
    today = datetime.now().date()
    
    # Extract birth month and day
    birth_month = birth_date.month
    birth_day = birth_date.day
    
    # Calculate this year's birthday
    current_year = today.year
    
    # Handle leap year case for Feb 29 births
    try:
        this_year_birthday = datetime(current_year, birth_month, birth_day).date()
    except ValueError:  # Feb 29 in non-leap year
        # Move to Feb 28 in non-leap years
        this_year_birthday = datetime(current_year, 2, 28).date()
    
    # Check if this year's birthday has already passed
    if this_year_birthday >= today:
        next_birthday = this_year_birthday
    else:
        # Birthday has passed this year, calculate for next year
        next_year = current_year + 1
        try:
            next_birthday = datetime(next_year, birth_month, birth_day).date()
        except ValueError:  # Feb 29 in non-leap year
            next_birthday = datetime(next_year, 2, 28).date()
    
    # Calculate the difference in days
    days_until_birthday = (next_birthday - today).days
    
    return days_until_birthday

# Entry point: calculate_days_until_next_birthday(birth_date: datetime) -> int

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_21_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_days_until_next_birthday(birth_date):
    result = calculate_days_until_next_birthday(birth_date)
    formatted_result = format_value_dt(result, birth_date)
    log_file.write(formatted_result + "\n")

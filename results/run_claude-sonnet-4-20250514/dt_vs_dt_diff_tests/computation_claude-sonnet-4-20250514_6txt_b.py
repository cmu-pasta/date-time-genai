
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_age_in_days(birth_date: datetime, current_date: datetime) -> int:
    # Ensure current_date is after birth_date
    if current_date < birth_date:
        birth_date, current_date = current_date, birth_date
    
    # Calculate the difference in years
    years = current_date.year - birth_date.year
    
    # Adjust for month and day
    if current_date.month < birth_date.month or \
       (current_date.month == birth_date.month and current_date.day < birth_date.day):
        years -= 1
    
    # Calculate remaining months after accounting for complete years
    temp_date = datetime(birth_date.year + years, birth_date.month, birth_date.day)
    months = 0
    
    while temp_date.month != current_date.month or temp_date.year != current_date.year:
        if temp_date.month == 12:
            temp_date = datetime(temp_date.year + 1, 1, temp_date.day)
        else:
            # Handle month transitions carefully
            next_month = temp_date.month + 1
            next_year = temp_date.year
            try:
                temp_date = datetime(next_year, next_month, temp_date.day)
            except ValueError:  # Handle cases like Feb 29 -> Feb 28
                temp_date = datetime(next_year, next_month, min(temp_date.day, 28))
        months += 1
        
        if temp_date > current_date:
            months -= 1
            break
    
    # Calculate total days by getting the actual difference
    total_days = (current_date - birth_date).days
    
    return total_days

# Entry point: calculate_age_in_days(birth_date: datetime, current_date: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_6txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_age_in_days(birth_date, current_date):
    result = calculate_age_in_days(birth_date, current_date)
    formatted_result = format_value_dt(result, birth_date, current_date)
    log_file.write(formatted_result + "\n")

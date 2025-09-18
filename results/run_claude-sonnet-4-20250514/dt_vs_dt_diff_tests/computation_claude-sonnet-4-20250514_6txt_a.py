
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_age_in_years_months_days(birth_date: datetime, current_date: datetime) -> int:
    # Ensure current_date is after birth_date
    if current_date < birth_date:
        birth_date, current_date = current_date, birth_date
    
    # Calculate years
    years = current_date.year - birth_date.year
    
    # Adjust years if birthday hasn't occurred this year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        years -= 1
    
    # Calculate months
    months = current_date.month - birth_date.month
    if current_date.day < birth_date.day:
        months -= 1
    if months < 0:
        months += 12
    
    # Calculate days
    if current_date.day >= birth_date.day:
        days = current_date.day - birth_date.day
    else:
        # Need to borrow from previous month
        # Create a date for the previous month to get its number of days
        if current_date.month == 1:
            prev_month_year = current_date.year - 1
            prev_month = 12
        else:
            prev_month_year = current_date.year
            prev_month = current_date.month - 1
        
        # Get the last day of the previous month
        from calendar import monthrange
        prev_month_days = monthrange(prev_month_year, prev_month)[1]
        days = prev_month_days - birth_date.day + current_date.day
    
    # Since we can only return simple types, we return years as the primary component
    # The full calculation gives us: years years, months months, days days
    # For demonstration, we return the years component
    return years

# Entry point: calculate_age_in_years_months_days(birth_date: datetime, current_date: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_6txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_age_in_years_months_days(birth_date, current_date):
    result = calculate_age_in_years_months_days(birth_date, current_date)
    formatted_result = format_value_dt(result, birth_date, current_date)
    log_file.write(formatted_result + "\n")

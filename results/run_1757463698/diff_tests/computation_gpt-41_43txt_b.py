
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_age_in_months(birthdate: date) -> int:
    # Step 1: Get today's date
    today = date.today()
    
    # Step 2: Calculate the difference in years and months
    years_diff = today.year - birthdate.year
    months_diff = today.month - birthdate.month
    total_months = years_diff * 12 + months_diff
    
    # Step 3: Adjust if today's day is before the birthdate's day (month not fully completed)
    if today.day < birthdate.day:
        total_months -= 1
    
    # Step 4: Return the total months as integer
    return total_months

# Entry point: calculate_age_in_months(birthdate: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_43txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_age_in_months(birthdate):
    result = calculate_age_in_months(birthdate)
    formatted_result = format_value_dt(result, birthdate)
    log_file.write(formatted_result + "\n")

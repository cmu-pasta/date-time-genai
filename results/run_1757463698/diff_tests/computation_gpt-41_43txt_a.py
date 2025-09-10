
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def compute_age_in_months(birthdate: date) -> int:
    # Step 1: Get today's date
    today = date.today()
    
    # Step 2: Compute year and month difference
    years_diff = today.year - birthdate.year
    months_diff = today.month - birthdate.month
    
    # Step 3: Total months difference
    total_months = years_diff * 12 + months_diff
    
    # Step 4: Adjust if current day has not reached birth day yet (partial month not counted)
    if today.day < birthdate.day:
        total_months -= 1
    
    # Step 5: Return the result
    return total_months

# Entry point: compute_age_in_months(birthdate: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_43txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_compute_age_in_months(birthdate):
    result = compute_age_in_months(birthdate)
    formatted_result = format_value_dt(result, birthdate)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def compute_age_in_years_months_days(birthdate: date) -> int:
    # Step 3: Get today's date
    today = date.today()
    
    # Step 4: Compute the preliminary difference
    years = today.year - birthdate.year
    months = today.month - birthdate.month
    days = today.day - birthdate.day
    
    # Step 5: Adjust for negative days
    if days < 0:
        # Borrow days from previous month
        # Calculate the number of days in the previous month
        if today.month == 1:
            prev_month = 12
            prev_year = today.year - 1
        else:
            prev_month = today.month - 1
            prev_year = today.year
        from calendar import monthrange
        days_in_prev_month = monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
        months -= 1

    # Step 5: Adjust for negative months
    if months < 0:
        months += 12
        years -= 1

    # Since the output type cannot be a tuple (per constraints), we'll encode the three values as a single integer.
    # For clarity, we'll return years*10000 + months*100 + days  (e.g. 21 years, 5 months, 12 days = 210512).
    return years * 10000 + months * 100 + days

# Entry point: compute_age_in_years_months_days(birthdate: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_4txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_compute_age_in_years_months_days(birthdate):
    result = compute_age_in_years_months_days(birthdate)
    formatted_result = format_value_dt(result, birthdate)
    log_file.write(formatted_result + "\n")

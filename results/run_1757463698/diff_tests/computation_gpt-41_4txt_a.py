
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def compute_age_ymd(birthdate: date) -> int:
    today = date.today()
    
    # Initial difference
    years = today.year - birthdate.year
    months = today.month - birthdate.month
    days = today.day - birthdate.day

    # Adjust days and months if needed
    if days < 0:
        # Borrow days from previous month
        # Calculate the number of days in the previous month
        if today.month == 1:
            prev_month = 12
            prev_month_year = today.year - 1
        else:
            prev_month = today.month - 1
            prev_month_year = today.year

        # Days in previous month
        if prev_month == 2:
            # Leap year check for February
            if (prev_month_year % 4 == 0 and prev_month_year % 100 != 0) or (prev_month_year % 400 == 0):
                days_in_prev_month = 29
            else:
                days_in_prev_month = 28
        elif prev_month in [1,3,5,7,8,10,12]:
            days_in_prev_month = 31
        else:
            days_in_prev_month = 30

        days += days_in_prev_month
        months -= 1

    if months < 0:
        months += 12
        years -= 1

    # The function returns years first, then months, then days as separate ints
    # Entry point expects a single output value, so we return years * 10000 + months * 100 + days as a combined integer
    return years * 10000 + months * 100 + days

# Entry point: compute_age_ymd(birthdate: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_4txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_compute_age_ymd(birthdate):
    result = compute_age_ymd(birthdate)
    formatted_result = format_value_dt(result, birthdate)
    log_file.write(formatted_result + "\n")

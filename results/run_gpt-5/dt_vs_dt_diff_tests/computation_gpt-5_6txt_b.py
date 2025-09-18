
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_age_ymd(start: date, end: date) -> int:
    """
    Calculate the age difference between two dates in years, months, and days.
    Returns a single integer encoded as YYYYMMDD (years*10000 + months*100 + days).

    - Input types: datetime.date
    - Output type: integer
    """
    # Ensure chronological order
    if end < start:
        start, end = end, start

    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day

    # Adjust days by borrowing from the previous month when negative
    if days < 0:
        first_of_end_month = date(end.year, end.month, 1)
        last_of_prev_month = first_of_end_month - timedelta(days=1)
        days += last_of_prev_month.day
        months -= 1

    # Adjust months by borrowing a year when negative
    if months < 0:
        months += 12
        years -= 1

    # Encode as YYYYMMDD
    return years * 10000 + months * 100 + days

# Entry point: calculate_age_ymd(start: date, end: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_6txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_age_ymd(start, end):
    result = calculate_age_ymd(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")

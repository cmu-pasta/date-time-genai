
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_age_ymd(d1: date, d2: date) -> int:
    # Ensure start <= end
    if d1 <= d2:
        start, end = d1, d2
    else:
        start, end = d2, d1

    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day

    # Adjust days by borrowing from the previous month if needed
    if days < 0:
        # Last day of the month preceding 'end'
        last_day_prev_month = (date(end.year, end.month, 1) - timedelta(days=1))
        days += last_day_prev_month.day
        months -= 1

    # Adjust months by borrowing from years if needed
    if months < 0:
        months += 12
        years -= 1

    # Encode as YYYYMMDD integer
    return years * 10000 + months * 100 + days

# Entry point: calculate_age_ymd(d1: date, d2: date) -> int

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_6_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_age_ymd(d1, d2):
    result = calculate_age_ymd(d1, d2)
    formatted_result = format_value_dt(result, d1, d2)
    log_file.write(formatted_result + "\n")

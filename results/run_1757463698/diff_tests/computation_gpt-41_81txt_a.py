
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_fridays_between(start_date: date, end_date: date) -> int:
    # Step 1: Ensure start_date is not after end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    # Step 2: Find the first Friday on or after start_date
    days_until_friday = (4 - start_date.weekday()) % 7  # Friday is weekday 4
    first_friday = start_date + timedelta(days=days_until_friday)

    # If first_friday is after end_date, there are no Fridays between the dates
    if first_friday > end_date:
        return 0

    # Step 3: Calculate number of whole weeks (i.e., Fridays) between first_friday and end_date
    total_days = (end_date - first_friday).days
    friday_count = 1 + (total_days // 7)  # Include the first Friday and count all subsequent Fridays

    # Step 4: Return the count as an integer
    return friday_count

# Entry point: count_fridays_between(start_date: date, end_date: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_81txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_fridays_between(start_date, end_date):
    result = count_fridays_between(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")

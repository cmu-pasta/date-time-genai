
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def nth_previous_business_day(start_date: date, n: int) -> date:
    """
    Returns the 'nth' previous business day from a given date.
    Business days are Monday to Friday. Weekends are skipped.
    
    Args:
        start_date (date): The date to count back from (exclusive).
        n (int): Number of business days to go back.
        
    Returns:
        date: The nth previous business day.
    """
    count = 0
    current_date = start_date
    while count < n:
        current_date -= timedelta(days=1)
        # weekday() returns 0 for Monday through 6 for Sunday
        if current_date.weekday() < 5:
            count += 1
    return current_date

# Entry point: nth_previous_business_day(start_date: date, n: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_80txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_nth_previous_business_day(start_date, n):
    result = nth_previous_business_day(start_date, n)
    formatted_result = format_value_dt(result, start_date, n)
    log_file.write(formatted_result + "\n")

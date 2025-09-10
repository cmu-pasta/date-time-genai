
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def days_until_next_holiday(current_date: date, holiday_month: int, holiday_day: int) -> int:
    # Step 1: Construct the holiday date for the current year
    holiday_this_year = date(current_date.year, holiday_month, holiday_day)
    
    # Step 2: If the holiday has already occurred this year, use next year
    if holiday_this_year < current_date:
        holiday_next = date(current_date.year + 1, holiday_month, holiday_day)
    else:
        holiday_next = holiday_this_year
    
    # Step 3: Calculate the difference in days
    delta = (holiday_next - current_date).days
    
    # Step 4: Return the result as an integer
    return delta

# Entry point: days_until_next_holiday(current_date: date, holiday_month: int, holiday_day: int) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_14txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy(), timestamp_strategy())
def test_days_until_next_holiday(current_date, holiday_month, holiday_day):
    result = days_until_next_holiday(current_date, holiday_month, holiday_day)
    formatted_result = format_value_dt(result, current_date, holiday_month, holiday_day)
    log_file.write(formatted_result + "\n")

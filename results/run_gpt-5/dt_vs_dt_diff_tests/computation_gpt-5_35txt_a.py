
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def last_business_day_of_month(year: int, month: int) -> date:
    """
    Return the last business day (Mon-Fri) of the given month and year.
    Business days exclude Saturdays and Sundays. Holidays are not considered.
    """
    # Step 1: Determine the first day of the next month
    if month == 12:
        first_of_next = date(year + 1, 1, 1)
    else:
        first_of_next = date(year, month + 1, 1)
    
    # Step 2: Last calendar day of the target month
    last_calendar_day = first_of_next - timedelta(days=1)
    
    # Step 3: Adjust back to the last business day if weekend
    # weekday(): Monday=0 ... Sunday=6
    wd = last_calendar_day.weekday()
    if wd == 6:  # Sunday
        last_business = last_calendar_day - timedelta(days=2)
    elif wd == 5:  # Saturday
        last_business = last_calendar_day - timedelta(days=1)
    else:
        last_business = last_calendar_day
    
    return last_business

# Entry point: last_business_day_of_month(year: int, month: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_35txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_last_business_day_of_month(year, month):
    result = last_business_day_of_month(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")

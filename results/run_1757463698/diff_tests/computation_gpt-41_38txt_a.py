
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def get_weeks_start_sunday(input_date: date) -> date:
    """
    Returns the start date of the week (Sunday) for a given input_date.
    
    Args:
        input_date (date): The input date.
    
    Returns:
        date: The date corresponding to the week's Sunday.
    """
    # Step 1: Calculate the number of days since the previous Sunday
    days_since_sunday = (input_date.weekday() + 1) % 7  # weekday(): Mon=0,...,Sun=6
    
    # Step 2: Subtract that many days to get the week's start date (Sunday)
    week_start = input_date - timedelta(days=days_since_sunday)
    
    # Step 3: Return the calculated date
    return week_start

# Entry point: get_weeks_start_sunday(input_date: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_38txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_get_weeks_start_sunday(input_date):
    result = get_weeks_start_sunday(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")

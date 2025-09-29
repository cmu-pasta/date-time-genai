
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_indigenous_peoples_day(year: int) -> date:
    """
    Return the date of Indigenous Peoples' Day for the given year.
    Indigenous Peoples' Day is observed on the second Monday of October.
    """
    # Step 1: Create a date for October 1st of the given year
    oct_first = date(year, 10, 1)
    
    # Step 2: Determine the weekday of October 1st (Monday=0, Sunday=6)
    weekday_oct_first = oct_first.weekday()
    
    # Step 3: Calculate days to the first Monday in October
    days_to_first_monday = (0 - weekday_oct_first) % 7  # 0 represents Monday
    first_monday = oct_first + timedelta(days=days_to_first_monday)
    
    # Step 4: The second Monday is 7 days after the first Monday
    second_monday = first_monday + timedelta(days=7)
    
    # Step 5: Return the date of Indigenous Peoples' Day
    return second_monday

# Entry point: calculate_indigenous_peoples_day(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_98txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_calculate_indigenous_peoples_day(year):
    result = calculate_indigenous_peoples_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

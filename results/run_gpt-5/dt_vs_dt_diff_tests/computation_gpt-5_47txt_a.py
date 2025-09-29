
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def memorial_day(year: int) -> date:
    """
    Compute the date of Memorial Day for a given year.
    Memorial Day is observed on the last Monday of May.
    
    Parameters:
        year (int): The target year (e.g., 2025)
    
    Returns:
        date: The date of Memorial Day in the given year.
    """
    # Step 1: Create the date for May 31st of the given year
    may_31 = date(year, 5, 31)
    
    # Step 2: Monday is 0, Sunday is 6. Find weekday of May 31
    weekday_may_31 = may_31.weekday()
    
    # Step 3: Compute offset to the most recent Monday (including May 31 if it is Monday)
    offset_days = (weekday_may_31 - 0) % 7  # 0 for Monday
    
    # Step 4: Subtract offset to get the last Monday of May
    memorial_day_date = may_31 - timedelta(days=offset_days)
    
    # Step 5: Return the computed date
    return memorial_day_date

# Entry point: memorial_day(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_47txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_memorial_day(year):
    result = memorial_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

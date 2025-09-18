
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def columbus_day(year: int) -> date:
    """
    Compute the date of Columbus Day for a given year.
    Columbus Day is observed on the second Monday of October.
    
    Parameters:
        year (int): The year for which to compute Columbus Day.
    
    Returns:
        date: The date of Columbus Day in the given year.
    """
    # October 1st of the given year
    oct_first = date(year, 10, 1)
    
    # Weekday of October 1st (Monday=0, Sunday=6)
    weekday_oct_first = oct_first.weekday()
    
    # Days to add to reach the first Monday in October
    days_to_first_monday = (0 - weekday_oct_first) % 7
    
    # First Monday in October
    first_monday = oct_first + timedelta(days=days_to_first_monday)
    
    # Second Monday in October (Columbus Day)
    columbus_day_date = first_monday + timedelta(days=7)
    
    return columbus_day_date

# Entry point: columbus_day(year: int) -> date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_77txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_columbus_day(year):
    result = columbus_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

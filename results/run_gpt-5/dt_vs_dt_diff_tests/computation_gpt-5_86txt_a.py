
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def presidents_day(year: int) -> date:
    """
    Compute the date of Presidents' Day (third Monday of February) for a given year.
    
    Parameters:
    - year: int, the Gregorian calendar year
    
    Returns:
    - date object representing Presidents' Day for the given year
    """
    # February 1st of the given year
    feb_first = date(year, 2, 1)
    
    # Monday is 0 per date.weekday(); compute days to the first Monday
    days_to_monday = (0 - feb_first.weekday()) % 7
    first_monday = feb_first + timedelta(days=days_to_monday)
    
    # Third Monday is 14 days after the first Monday
    third_monday = first_monday + timedelta(days=14)
    return third_monday

# Entry point: presidents_day(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_86txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_presidents_day(year):
    result = presidents_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

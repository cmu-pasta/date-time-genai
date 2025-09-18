
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def indigenous_peoples_day(year: int) -> date:
    """
    Calculate Indigenous Peoples' Day (second Monday of October) for a given year.
    
    Args:
        year (int): The year for which to compute the holiday.
    
    Returns:
        date: The date of Indigenous Peoples' Day in the given year.
    """
    # October 1st of the given year
    oct_first = date(year, 10, 1)
    
    # Weekday: Monday=0, Sunday=6. Compute days to the first Monday in October.
    days_to_first_monday = (0 - oct_first.weekday()) % 7
    first_monday = oct_first + timedelta(days=days_to_first_monday)
    
    # Indigenous Peoples' Day is the second Monday in October
    second_monday = first_monday + timedelta(days=7)
    return second_monday

# Entry point: indigenous_peoples_day(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_98txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_indigenous_peoples_day(year):
    result = indigenous_peoples_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

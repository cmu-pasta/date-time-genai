
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def mlk_day(year: int) -> date:
    """
    Compute Martin Luther King Jr. Day for a given year.
    MLK Day is observed on the third Monday of January.
    """
    # January 1st of the given year
    jan1 = date(year, 1, 1)
    
    # Determine days to the first Monday (Monday=0, Sunday=6)
    days_to_first_monday = (0 - jan1.weekday()) % 7
    
    # First Monday in January
    first_monday = jan1 + timedelta(days=days_to_first_monday)
    
    # Third Monday = first Monday + 14 days
    mlk = first_monday + timedelta(days=14)
    return mlk

# Entry point: mlk_day(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_92txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_mlk_day(year):
    result = mlk_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

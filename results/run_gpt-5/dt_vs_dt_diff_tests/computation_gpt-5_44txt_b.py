
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def first_day_of_spring(year: int, northern_hemisphere: bool) -> date:
    """
    Return the date of the first day of spring for a given year using the meteorological definition.
    
    Parameters:
    - year: integer year (e.g., 2025)
    - northern_hemisphere: boolean; True for Northern Hemisphere, False for Southern Hemisphere
    
    Returns:
    - datetime.date representing the first day of spring for the specified hemisphere and year.
      Northern Hemisphere: March 1
      Southern Hemisphere: September 1
    """
    if northern_hemisphere:
        return date(year, 3, 1)
    else:
        return date(year, 9, 1)

# Entry point: first_day_of_spring(year: int, northern_hemisphere: bool) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_44txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), bool_strategy())
def test_first_day_of_spring(year, northern_hemisphere):
    result = first_day_of_spring(year, northern_hemisphere)
    formatted_result = format_value_dt(result, year, northern_hemisphere)
    log_file.write(formatted_result + "\n")

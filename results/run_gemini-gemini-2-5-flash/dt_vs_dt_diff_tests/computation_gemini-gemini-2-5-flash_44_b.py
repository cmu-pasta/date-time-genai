
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def get_first_day_of_spring(year: int) -> date:
    # Step 1: Given the constraints (datetime library only, no complex data types for external data),
    # and the fact that the datetime library does not compute astronomical events,
    # we will use the most common date for the vernal equinox (first day of spring)
    # in the Northern Hemisphere, which is March 20th.
    
    # Step 2: Construct a date object for March 20th of the given year.
    first_day_of_spring = date(year, 3, 20)
    
    # Step 3: Return the date object.
    return first_day_of_spring

# Entry point: get_first_day_of_spring(year: int) -> date

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_44_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_get_first_day_of_spring(year):
    result = get_first_day_of_spring(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

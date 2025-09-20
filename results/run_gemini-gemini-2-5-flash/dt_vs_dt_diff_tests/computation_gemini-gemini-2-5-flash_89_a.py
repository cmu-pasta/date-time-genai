
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_nowruz_date(year: int) -> date:
    # Step 1: Nowruz typically falls on March 20th or March 21st, coinciding with the spring equinox.
    # Due to the constraint of using only the datetime library and not external astronomical
    # calculation libraries or lookup tables, we will use the most common date for Nowruz,
    # which is March 20th, for any given year.
    
    # Step 2: Create a date object for March 20th of the given year.
    nowruz_date = date(year, 3, 20)
    
    # Step 3: Return the calculated date.
    return nowruz_date

# Entry point: find_nowruz_date(year: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_89_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_nowruz_date(year):
    result = find_nowruz_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

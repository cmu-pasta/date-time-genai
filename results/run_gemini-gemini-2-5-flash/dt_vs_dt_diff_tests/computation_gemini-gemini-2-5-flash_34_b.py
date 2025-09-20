
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_date_to_day_of_year(dt: datetime) -> int:
    # Step 1: Get the time tuple for the given datetime object
    time_tuple = dt.timetuple()
    
    # Step 2: Extract the day of the year from the time tuple
    # tm_yday represents the day of the year as an integer (1-366)
    day_of_year = time_tuple.tm_yday
    
    # Step 3: Return the day of the year
    return day_of_year

# Entry point: convert_date_to_day_of_year(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_34_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_date_to_day_of_year(dt):
    result = convert_date_to_day_of_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

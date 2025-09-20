
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_presidents_day(year: int) -> datetime:
    # Step 1: Establish the base date as February 1st of the given year.
    feb_1st = datetime(year, 2, 1)
    
    # Step 2: Calculate the number of days to add to reach the first Monday of February.
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday.
    # To find the next Monday (or current day if it's Monday): (7 - current_weekday) % 7
    days_to_first_monday = (7 - feb_1st.weekday()) % 7
    
    # Step 3: Get the date of the first Monday in February.
    first_monday = feb_1st + timedelta(days=days_to_first_monday)
    
    # Step 4: Presidents' Day is the third Monday in February.
    # This is exactly two weeks (14 days) after the first Monday.
    presidents_day = first_monday + timedelta(weeks=2)
    
    # Step 5: Return the calculated date.
    return presidents_day

# Entry point: find_presidents_day(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_86_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_presidents_day(year):
    result = find_presidents_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

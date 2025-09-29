
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_thanksgiving_date(year: int) -> datetime:
    # Step 1: Get November 1st of the given year
    november_1st = datetime(year, 11, 1)
    
    # Step 2: Find what day of the week November 1st is (Monday=0, Sunday=6)
    november_1st_weekday = november_1st.weekday()
    
    # Step 3: Calculate days to add to get to the first Thursday (Thursday=3)
    days_to_first_thursday = (3 - november_1st_weekday) % 7
    
    # Step 4: Calculate the day number for the fourth Thursday
    # First Thursday + 21 days (3 weeks) = Fourth Thursday
    fourth_thursday_day = 1 + days_to_first_thursday + 21
    
    # Step 5: Create and return the datetime object for Thanksgiving
    thanksgiving_date = datetime(year, 11, fourth_thursday_day)
    
    return thanksgiving_date

# Entry point: find_thanksgiving_date(year: int) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_29_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_thanksgiving_date(year):
    result = find_thanksgiving_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

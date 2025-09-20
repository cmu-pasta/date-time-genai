
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_thanksgiving_date(year: int) -> date:
    # Step 1: Create a date object for November 1st of the given year
    november_first = date(year, 11, 1)
    
    # Step 2: Determine the weekday of November 1st. Monday is 0 and Sunday is 6.
    # We are looking for Thursday, which is 3.
    day_of_week_november_first = november_first.weekday()
    
    # Step 3: Calculate how many days to add to November 1st to get to the first Thursday.
    # (3 - day_of_week_november_first + 7) % 7 ensures a positive offset for the next Thursday.
    days_to_first_thursday = (3 - day_of_week_november_first + 7) % 7
    
    # Step 4: Calculate the date of the first Thursday in November
    first_thursday = november_first + timedelta(days=days_to_first_thursday)
    
    # Step 5: Thanksgiving is the fourth Thursday, so add 3 more weeks (21 days)
    thanksgiving_date = first_thursday + timedelta(days=21)
    
    # Step 6: Return the calculated date
    return thanksgiving_date

# Entry point: find_thanksgiving_date(year: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_29_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_thanksgiving_date(year):
    result = find_thanksgiving_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_presidents_day(year: int) -> date:
    # Step 1: Determine the first day of February for the given year
    feb_1st = date(year, 2, 1)
    
    # Step 2: Find the weekday of February 1st (Monday is 0, Sunday is 6)
    feb_1st_weekday = feb_1st.weekday()
    
    # Step 3: Calculate the number of days to add to get to the first Monday
    # (0 - feb_1st_weekday + 7) % 7 ensures we get the next Monday, or feb_1st itself if it's Monday
    days_to_first_monday = (0 - feb_1st_weekday + 7) % 7
    
    # Step 4: Calculate the date of the first Monday of February
    first_monday_of_feb = feb_1st + timedelta(days=days_to_first_monday)
    
    # Step 5: Presidents' Day is the third Monday, so add two weeks (14 days) to the first Monday
    presidents_day = first_monday_of_feb + timedelta(weeks=2)
    
    # Step 6: Return the calculated date
    return presidents_day

# Entry point: find_presidents_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_86_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_presidents_day(year):
    result = find_presidents_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

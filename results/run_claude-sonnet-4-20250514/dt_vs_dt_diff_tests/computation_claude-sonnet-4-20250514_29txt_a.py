
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_thanksgiving_date(year: int) -> date:
    # Step 1: Get November 1st of the given year
    november_1st = date(year, 11, 1)
    
    # Step 2: Find the first Thursday in November
    # Thursday is weekday 3 (Monday=0, Tuesday=1, Wednesday=2, Thursday=3, etc.)
    days_to_first_thursday = (3 - november_1st.weekday()) % 7
    first_thursday = november_1st + timedelta(days=days_to_first_thursday)
    
    # Step 3: Add 3 weeks (21 days) to get the fourth Thursday
    fourth_thursday = first_thursday + timedelta(days=21)
    
    # Step 4: Return the Thanksgiving date
    return fourth_thursday

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_29txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_thanksgiving_date(year):
    result = find_thanksgiving_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

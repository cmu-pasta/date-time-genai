
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_fortnights_difference(dt1: datetime, dt2: datetime) -> float:
    # Step 1: Calculate the absolute difference in days between the two datetime objects.
    # The .days attribute of a timedelta object gives the number of whole days.
    # We use abs() to handle cases where dt2 is earlier than dt1.
    total_days = abs((dt2 - dt1).days)
    
    # Step 2: Calculate the number of fortnights.
    # A fortnight is 14 days.
    number_of_fortnights = total_days / 14.0
    
    # Step 3: Return the result as a float.
    return number_of_fortnights

# Entry point: calculate_fortnights_difference(dt1: datetime, dt2: datetime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_63_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_fortnights_difference(dt1, dt2):
    result = calculate_fortnights_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")

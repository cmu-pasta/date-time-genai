
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_age_in_seconds(birth_dt: datetime) -> float:
    # Step 1: Get the current datetime
    # We use datetime.now() to get the current local datetime.
    current_dt = datetime.now()
    
    # Step 2: Calculate the difference between the current datetime and the birth datetime
    # This results in a timedelta object.
    time_difference = current_dt - birth_dt
    
    # Step 3: Convert the timedelta to total seconds
    # The total_seconds() method returns the total duration in seconds as a float.
    age_in_seconds = time_difference.total_seconds()
    
    # Step 4: Ensure the age is not negative (though for chronological age it should naturally be positive)
    # Using abs() to handle potential future dates as birth_dt, if that were a consideration,
    # but for "age" it should be a positive duration.
    return abs(age_in_seconds)

# Entry point: calculate_age_in_seconds(birth_dt: datetime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_75_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_age_in_seconds(birth_dt):
    result = calculate_age_in_seconds(birth_dt)
    formatted_result = format_value_dt(result, birth_dt)
    log_file.write(formatted_result + "\n")

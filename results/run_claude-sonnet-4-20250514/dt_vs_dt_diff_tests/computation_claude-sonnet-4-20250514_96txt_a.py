
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
import math
def calculate_equation_of_time(input_date: date) -> float:
    # Step 1: Get the day of year (1-366)
    day_of_year = input_date.timetuple().tm_yday
    
    # Step 2: Calculate B in radians
    # B = 360/365 * (day_of_year - 81) converted to radians
    B_degrees = (360.0 / 365.0) * (day_of_year - 81)
    B_radians = math.radians(B_degrees)
    
    # Step 3: Calculate the equation of time using the standard approximation
    # E = 9.87 * sin(2B) - 7.53 * cos(B) - 1.5 * sin(B)
    equation_of_time = (9.87 * math.sin(2 * B_radians) - 
                       7.53 * math.cos(B_radians) - 
                       1.5 * math.sin(B_radians))
    
    # Step 4: Return the correction in minutes
    return equation_of_time

# Entry point: calculate_equation_of_time(input_date: date) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_96txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_equation_of_time(input_date):
    result = calculate_equation_of_time(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")

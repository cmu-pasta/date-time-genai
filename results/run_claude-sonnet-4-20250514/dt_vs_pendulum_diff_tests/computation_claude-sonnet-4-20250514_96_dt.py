
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
import math
def calculate_equation_of_time(dt: datetime) -> float:
    # Step 1: Get the day of year (1-365 or 1-366 for leap years)
    day_of_year = dt.timetuple().tm_yday
    
    # Step 2: Calculate B (angle in radians)
    # B represents the angular position in Earth's orbit
    B = 2 * math.pi * (day_of_year - 81) / 365.25
    
    # Step 3: Apply the equation of time formula
    # This accounts for Earth's elliptical orbit and axial tilt
    # Result is in minutes
    equation_of_time = (9.87 * math.sin(2 * B) - 
                       7.53 * math.cos(B) - 
                       1.5 * math.sin(B))
    
    # Step 4: Return the equation of time correction in minutes
    return equation_of_time

# Entry point: calculate_equation_of_time(dt: datetime) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_96_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_equation_of_time(dt):
    result = calculate_equation_of_time(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

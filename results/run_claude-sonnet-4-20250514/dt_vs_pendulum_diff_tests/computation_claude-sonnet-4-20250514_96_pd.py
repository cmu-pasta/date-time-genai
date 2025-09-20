
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
import math
def calculate_equation_of_time(dt: pendulum.DateTime) -> float:
    # Step 1: Get the day of year (1-365/366)
    day_of_year = dt.day_of_year
    
    # Step 2: Calculate B in radians
    # B = 360 * (day_of_year - 81) / 365 degrees, converted to radians
    B_degrees = 360 * (day_of_year - 81) / 365
    B_radians = math.radians(B_degrees)
    
    # Step 3: Apply the equation of time formula
    # E = 9.87 * sin(2B) - 7.53 * cos(B) - 1.5 * sin(B)
    equation_of_time = (9.87 * math.sin(2 * B_radians) - 
                       7.53 * math.cos(B_radians) - 
                       1.5 * math.sin(B_radians))
    
    # Step 4: Return the result as a float (in minutes)
    return equation_of_time

# Entry point: calculate_equation_of_time(dt: pendulum.DateTime) -> float

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_96_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_equation_of_time(dt):
    result = calculate_equation_of_time(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")

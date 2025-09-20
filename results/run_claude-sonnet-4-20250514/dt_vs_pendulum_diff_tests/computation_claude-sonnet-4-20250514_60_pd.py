
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
import math
def calculate_solar_noon(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.DateTime:
    # Step 1: Get the day of year
    day_of_year = date.day_of_year
    
    # Step 2: Calculate the equation of time (in minutes)
    # This accounts for Earth's elliptical orbit and axial tilt
    B = 2 * math.pi * (day_of_year - 81) / 365
    equation_of_time = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    
    # Step 3: Calculate longitude correction (4 minutes per degree)
    # Assuming we're using local standard time zone
    time_zone_longitude = round(longitude / 15) * 15  # Standard meridian for the time zone
    longitude_correction = 4 * (longitude - time_zone_longitude)  # in minutes
    
    # Step 4: Calculate solar noon time
    # Start with 12:00 noon and apply corrections
    solar_noon_minutes = 12 * 60 + equation_of_time + longitude_correction
    
    # Step 5: Convert minutes to hours and minutes
    hours = int(solar_noon_minutes // 60)
    minutes = int(solar_noon_minutes % 60)
    seconds = int((solar_noon_minutes % 1) * 60)
    
    # Step 6: Create and return the solar noon datetime
    solar_noon_time = date.at(hours, minutes, seconds)
    
    return solar_noon_time

# Entry point: calculate_solar_noon(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_60_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_solar_noon(date, latitude, longitude):
    result = calculate_solar_noon(date, latitude, longitude)
    formatted_result = format_value_pd(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")

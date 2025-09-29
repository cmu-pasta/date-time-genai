
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
import math
def calculate_sunset_time(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.DateTime:
    # Convert date to day of year
    day_of_year = date.day_of_year
    
    # Calculate solar declination angle (approximation)
    declination = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
    
    # Convert latitude to radians
    lat_rad = math.radians(latitude)
    decl_rad = math.radians(declination)
    
    # Calculate hour angle for sunset
    try:
        cos_hour_angle = -math.tan(lat_rad) * math.tan(decl_rad)
        # Clamp the value to avoid math domain errors
        cos_hour_angle = max(-1, min(1, cos_hour_angle))
        hour_angle = math.degrees(math.acos(cos_hour_angle))
    except ValueError:
        # Handle polar day/night cases - assume 6 PM as default
        hour_angle = 90
    
    # Calculate sunset time in hours from solar noon
    sunset_hour_decimal = 12 + hour_angle / 15
    
    # Apply longitude correction (4 minutes per degree)
    longitude_correction = longitude / 15
    local_sunset_hour = sunset_hour_decimal - longitude_correction
    
    # Ensure the hour is within 0-24 range
    local_sunset_hour = local_sunset_hour % 24
    
    # Convert decimal hour to hours and minutes
    sunset_hour = int(local_sunset_hour)
    sunset_minute = int((local_sunset_hour - sunset_hour) * 60)
    
    # Create the sunset datetime
    sunset_datetime = pendulum.datetime(date.year, date.month, date.day, sunset_hour, sunset_minute, 0)
    
    return sunset_datetime

# Entry point: calculate_sunset_time(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_84_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_sunset_time(date, latitude, longitude):
    result = calculate_sunset_time(date, latitude, longitude)
    formatted_result = format_value_pd(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")

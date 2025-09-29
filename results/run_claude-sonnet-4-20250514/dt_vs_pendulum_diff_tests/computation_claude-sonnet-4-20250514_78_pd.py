
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
import math
def calculate_sunrise_time(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.DateTime:
    # Step 1: Calculate day of year
    day_of_year = date.day_of_year
    
    # Step 2: Calculate solar declination (in radians)
    solar_declination = math.radians(23.45) * math.sin(math.radians(360 * (284 + day_of_year) / 365))
    
    # Step 3: Convert latitude to radians
    lat_radians = math.radians(latitude)
    
    # Step 4: Calculate hour angle for sunrise
    try:
        hour_angle_cos = -math.tan(lat_radians) * math.tan(solar_declination)
        # Check if sun rises (polar regions might not have sunrise)
        if hour_angle_cos > 1 or hour_angle_cos < -1:
            # Sun doesn't rise or set, return noon as approximation
            hour_angle = 0
        else:
            hour_angle = math.degrees(math.acos(hour_angle_cos))
    except:
        hour_angle = 0
    
    # Step 5: Calculate sunrise time in hours (solar time)
    sunrise_solar_time = 12 - hour_angle / 15
    
    # Step 6: Adjust for longitude (4 minutes per degree)
    longitude_correction = longitude / 15
    sunrise_local_time = sunrise_solar_time - longitude_correction
    
    # Step 7: Convert hours to hours and minutes
    sunrise_hours = int(sunrise_local_time)
    sunrise_minutes = int((sunrise_local_time - sunrise_hours) * 60)
    
    # Step 8: Create pendulum.DateTime object
    sunrise_datetime = date.at(sunrise_hours, sunrise_minutes, 0)
    
    return sunrise_datetime

# Entry point: calculate_sunrise_time(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_78_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_sunrise_time(date, latitude, longitude):
    result = calculate_sunrise_time(date, latitude, longitude)
    formatted_result = format_value_pd(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")


import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
import math
def calculate_solar_noon(d: pendulum.Date, latitude: float, longitude: float, tz: pendulum.Timezone) -> pendulum.DateTime:
    # Step 1: Compute day of year
    N = d.day_of_year
    
    # Step 2: Fractional year (radians), evaluated at local solar noon reference
    gamma = (2.0 * math.pi / 365.0) * (N - 1)
    
    # Step 3: Equation of Time (minutes) using a common approximation
    eot = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2.0 * gamma)
        - 0.040849 * math.sin(2.0 * gamma)
    )
    
    # Step 4: Local timezone offset in minutes for the given date (includes DST if applicable)
    local_noon_anchor = pendulum.datetime(d.year, d.month, d.day, 12, 0, 0, tz=tz)
    tz_offset_minutes = int(local_noon_anchor.utcoffset().total_seconds() // 60)
    
    # Step 5: Solar noon minutes from local midnight
    # Longitude in degrees, positive east of Greenwich (negative for west).
    solar_noon_minutes = 720.0 - 4.0 * longitude - eot + tz_offset_minutes
    
    # Step 6: Build the solar noon DateTime in the given timezone
    base_midnight = pendulum.datetime(d.year, d.month, d.day, 0, 0, 0, tz=tz)
    solar_noon_dt = base_midnight + pendulum.duration(seconds=int(round(solar_noon_minutes * 60.0)))
    
    return solar_noon_dt

# Entry point: calculate_solar_noon(d: pendulum.Date, latitude: float, longitude: float, tz: pendulum.Timezone) -> pendulum.DateTime

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_60_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_solar_noon(d, latitude, longitude, tz):
    result = calculate_solar_noon(d, latitude, longitude, tz)
    formatted_result = format_value_pd(result, d, latitude, longitude, tz)
    log_file.write(formatted_result + "\n")

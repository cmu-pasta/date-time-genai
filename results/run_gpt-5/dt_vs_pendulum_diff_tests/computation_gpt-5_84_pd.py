
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import math
import pendulum
def calculate_sunset(date: pendulum.Date, latitude: float, longitude: float, tz: pendulum.Timezone) -> pendulum.DateTime:
    # Constants
    zenith = 90.833  # standard zenith for civil sunrise/sunset
    
    # Helpers
    def deg_to_rad(d: float) -> float:
        return d * math.pi / 180.0

    def rad_to_deg(r: float) -> float:
        return r * 180.0 / math.pi

    def normalize_angle(angle: float) -> float:
        # Normalize to [0, 360)
        return angle % 360.0

    # 1) Day of year
    N = date.day_of_year

    # 2) Convert the longitude to hour value
    lng_hour = longitude / 15.0

    # 3) Approximate time for sunset (18 is 6 PM local solar time)
    t = N + ((18.0 - lng_hour) / 24.0)

    # 4) Sun's mean anomaly
    M = (0.9856 * t) - 3.289

    # 5) Sun's true longitude L
    L = M + (1.916 * math.sin(deg_to_rad(M))) + (0.020 * math.sin(2 * deg_to_rad(M))) + 282.634
    L = normalize_angle(L)

    # 6) Sun's right ascension RA
    RA = rad_to_deg(math.atan(0.91764 * math.tan(deg_to_rad(L))))
    RA = normalize_angle(RA)

    # Adjust RA to be in the same quadrant as L
    L_quadrant = (math.floor(L / 90.0)) * 90.0
    RA_quadrant = (math.floor(RA / 90.0)) * 90.0
    RA = RA + (L_quadrant - RA_quadrant)

    # Convert RA to hours
    RA_hours = RA / 15.0

    # 7) Sun's declination
    sin_dec = 0.39782 * math.sin(deg_to_rad(L))
    cos_dec = math.cos(math.asin(sin_dec))

    # 8) Sun's local hour angle
    cos_h = (math.cos(deg_to_rad(zenith)) - (sin_dec * math.sin(deg_to_rad(latitude)))) / (cos_dec * math.cos(deg_to_rad(latitude)))

    # Handle polar day/night conditions
    if cos_h > 1.0:
        raise ValueError("The sun never rises on this date at the given location (no sunset can be computed).")
    if cos_h < -1.0:
        raise ValueError("The sun never sets on this date at the given location.")

    # For sunset
    H = rad_to_deg(math.acos(cos_h))  # in degrees
    H_hours = H / 15.0

    # 9) Local mean time of setting
    T_local = H_hours + RA_hours - (0.06571 * t) - 6.622

    # 10) Convert to UTC
    UT = T_local - lng_hour
    # Normalize UT to [0, 24)
    UT = UT % 24.0

    # 11) Build UTC DateTime from fractional hours
    hour = int(UT)
    minute = int((UT - hour) * 60.0)
    second = int(round((((UT - hour) * 60.0) - minute) * 60.0))

    # Normalize seconds/minutes rollover
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour = (hour + 1) % 24

    dt_utc = pendulum.datetime(date.year, date.month, date.day, hour, minute, second, tz="UTC")

    # 12) Convert to the requested timezone
    dt_local = dt_utc.in_timezone(tz)

    return dt_local

# Entry point: calculate_sunset(date: pendulum.Date, latitude: float, longitude: float, tz: pendulum.Timezone) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_84_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_sunset(date, latitude, longitude, tz):
    result = calculate_sunset(date, latitude, longitude, tz)
    formatted_result = format_value_pd(result, date, latitude, longitude, tz)
    log_file.write(formatted_result + "\n")

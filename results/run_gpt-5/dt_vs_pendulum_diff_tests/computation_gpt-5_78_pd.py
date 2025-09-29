
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import math
import pendulum
def _normalize_degrees(angle: float) -> float:
    a = angle % 360.0
    if a < 0:
        a += 360.0
    return a

def _deg_to_rad(deg: float) -> float:
    return deg * math.pi / 180.0

def _rad_to_deg(rad: float) -> float:
    return rad * 180.0 / math.pi

def calculate_sunrise(date: pendulum.Date, latitude: float, longitude: float, tz: pendulum.Timezone) -> pendulum.DateTime:
    # NOAA Sunrise Algorithm
    N = date.day_of_year  # day of year

    lngHour = longitude / 15.0

    # Approximate time for sunrise (6h local solar time)
    t = N + ((6.0 - lngHour) / 24.0)

    # Sun's mean anomaly
    M = (0.9856 * t) - 3.289

    # Sun's true longitude
    L = M + (1.916 * math.sin(_deg_to_rad(M))) + (0.020 * math.sin(_deg_to_rad(2 * M))) + 282.634
    L = _normalize_degrees(L)

    # Sun's right ascension
    RA = _rad_to_deg(math.atan(0.91764 * math.tan(_deg_to_rad(L))))
    RA = _normalize_degrees(RA)

    # Adjust RA to be in the same quadrant as L
    Lquadrant  = math.floor(L / 90.0) * 90.0
    RAquadrant = math.floor(RA / 90.0) * 90.0
    RA = RA + (Lquadrant - RAquadrant)

    # Convert RA into hours
    RA /= 15.0

    # Sun's declination
    sinDec = 0.39782 * math.sin(_deg_to_rad(L))
    cosDec = math.cos(math.asin(sinDec))

    # Sun's local hour angle
    cosH = (math.cos(_deg_to_rad(90.833)) - (sinDec * math.sin(_deg_to_rad(latitude)))) / (cosDec * math.cos(_deg_to_rad(latitude)))

    if cosH > 1.0:
        raise ValueError("Sun never rises on this date at this latitude.")
    if cosH < -1.0:
        raise ValueError("Sun never sets on this date at this latitude; sunrise does not occur.")

    # For sunrise, H = 360 - arccos(cosH)
    H = 360.0 - _rad_to_deg(math.acos(cosH))
    H /= 15.0  # convert to hours

    # Local mean time of rising
    T = H + RA - (0.06571 * t) - 6.622

    # Convert to UTC
    UT = T - lngHour
    UT = (UT + 24.0) % 24.0  # normalize to [0,24)

    # Build a UTC datetime for the given date at UT hours
    hour = int(UT)
    minute = int((UT - hour) * 60.0)
    second = int(round((((UT - hour) * 60.0) - minute) * 60.0))

    # Normalize possible rounding overflow
    total_seconds = hour * 3600 + minute * 60 + second
    if total_seconds >= 86400:
        total_seconds -= 86400
    hour = total_seconds // 3600
    minute = (total_seconds % 3600) // 60
    second = total_seconds % 60

    sunrise_utc = pendulum.datetime(date.year, date.month, date.day, hour, minute, second, tz="UTC")

    # Convert to requested timezone
    sunrise_local = sunrise_utc.in_timezone(tz)

    return sunrise_local

# Entry point: calculate_sunrise(date: pendulum.Date, latitude: float, longitude: float, tz: pendulum.Timezone) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_78_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_sunrise(date, latitude, longitude, tz):
    result = calculate_sunrise(date, latitude, longitude, tz)
    formatted_result = format_value_pd(result, date, latitude, longitude, tz)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo
import math
def calculate_sunrise(given_date: date, latitude: float, longitude: float, target_tz: ZoneInfo) -> datetime:
    # Constants
    zenith = 90.833  # degrees, official sunrise
    deg_to_rad = math.pi / 180.0
    rad_to_deg = 180.0 / math.pi

    # 1) Day of year
    n = given_date.timetuple().tm_yday

    # 2) Longitude hour
    lng_hour = longitude / 15.0

    # 3) Approximate time for sunrise
    t = n + ((6.0 - lng_hour) / 24.0)

    # 4) Sun's mean anomaly
    M = (0.9856 * t) - 3.289

    # 5) Sun's true longitude
    L = M + (1.916 * math.sin(M * deg_to_rad)) + (0.020 * math.sin(2 * M * deg_to_rad)) + 282.634
    L = (L + 360.0) % 360.0  # normalize to [0, 360)

    # 6) Sun's right ascension
    RA = math.atan(0.91764 * math.tan(L * deg_to_rad)) * rad_to_deg
    RA = (RA + 360.0) % 360.0

    # Adjust RA to be in the same quadrant as L
    L_quadrant = math.floor(L / 90.0) * 90.0
    RA_quadrant = math.floor(RA / 90.0) * 90.0
    RA = RA + (L_quadrant - RA_quadrant)

    # Convert RA to hours
    RA = RA / 15.0

    # 7) Sun's declination
    sinDec = 0.39782 * math.sin(L * deg_to_rad)
    cosDec = math.cos(math.asin(sinDec))

    # 8) Sun's local hour angle for sunrise
    cosH = (math.cos(zenith * deg_to_rad) - (sinDec * math.sin(latitude * deg_to_rad))) / (cosDec * math.cos(latitude * deg_to_rad))

    # Check for polar day/night conditions
    if cosH > 1.0:
        raise ValueError("Sun never rises on this date at this location.")
    if cosH < -1.0:
        # Sun never sets; sunrise is undefined
        raise ValueError("Sun never sets on this date at this location; sunrise is undefined.")

    # For sunrise, H = 360 - arccos(cosH)
    H = 360.0 - (math.acos(cosH) * rad_to_deg)
    H = H / 15.0  # convert to hours

    # 9) Local mean time of rising
    T = H + RA - (0.06571 * t) - 6.622

    # 10) UTC time
    UT = T - lng_hour
    UT = (UT % 24.0 + 24.0) % 24.0  # normalize to [0, 24)

    # Convert fractional hours to hh:mm:ss
    hour = int(UT)
    minute_float = (UT - hour) * 60.0
    minute = int(minute_float)
    second = int(round((minute_float - minute) * 60.0))

    # Handle rounding that may push seconds/minutes over their bounds
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour = (hour + 1) % 24

    # Build UTC datetime and convert to target timezone
    sunrise_utc = datetime(given_date.year, given_date.month, given_date.day, hour, minute, second, tzinfo=timezone.utc)
    sunrise_local = sunrise_utc.astimezone(target_tz)
    return sunrise_local

# Entry point: calculate_sunrise(given_date: date, latitude: float, longitude: float, target_tz: ZoneInfo) -> datetime

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_78_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_sunrise(given_date, latitude, longitude, target_tz):
    result = calculate_sunrise(given_date, latitude, longitude, target_tz)
    formatted_result = format_value_dt(result, given_date, latitude, longitude, target_tz)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timedelta, time
from zoneinfo import ZoneInfo
import math
def calculate_sunset(dt: date, latitude: float, longitude: float, tz: ZoneInfo) -> datetime:
    # Helper conversions between degrees and radians
    def deg_to_rad(deg: float) -> float:
        return deg * math.pi / 180.0

    def rad_to_deg(rad: float) -> float:
        return rad * 180.0 / math.pi

    def normalize_deg(deg: float) -> float:
        # Normalize degrees to [0, 360)
        return deg % 360.0

    # 1) Day of year
    N = dt.timetuple().tm_yday

    # 2) Longitude to hour value
    lngHour = longitude / 15.0

    # 3) Approximate time for sunset (18:00 local solar time)
    t = N + ((18.0 - lngHour) / 24.0)

    # 4) Sun's mean anomaly
    M = (0.9856 * t) - 3.289

    # 5) Sun's true longitude (L), normalized
    L = M + (1.916 * math.sin(deg_to_rad(M))) + (0.020 * math.sin(2 * deg_to_rad(M))) + 282.634
    L = normalize_deg(L)

    # 6) Sun's right ascension (RA)
    RA = rad_to_deg(math.atan(0.91764 * math.tan(deg_to_rad(L))))
    RA = normalize_deg(RA)

    # Adjust RA to be in the same quadrant as L
    L_quadrant = (math.floor(L / 90.0)) * 90.0
    RA_quadrant = (math.floor(RA / 90.0)) * 90.0
    RA = RA + (L_quadrant - RA_quadrant)

    # Convert RA to hours
    RA = RA / 15.0

    # 7) Sun's declination
    sinDec = 0.39782 * math.sin(deg_to_rad(L))
    cosDec = math.cos(math.asin(sinDec))

    # 8) Sun's local hour angle for sunset
    cosH = (math.cos(deg_to_rad(90.833)) - (sinDec * math.sin(deg_to_rad(latitude)))) / (cosDec * math.cos(deg_to_rad(latitude)))

    # Check for polar conditions
    if cosH < -1.0:
        # Sun never sets on this date at this location
        raise ValueError("Sun never sets on the given date at the specified location.")
    if cosH > 1.0:
        # Sun never rises on this date at this location
        raise ValueError("Sun never rises on the given date at the specified location.")

    # For sunset, H = arccos(cosH) in degrees
    H = rad_to_deg(math.acos(cosH))
    H = H / 15.0  # convert to hours

    # 9) Local mean time of setting
    T = H + RA - (0.06571 * t) - 6.622

    # 10) Convert to UT
    UT = T - lngHour
    # Normalize UT to [0, 24)
    UT = UT % 24.0

    # 11) Build UTC datetime and convert to requested timezone
    utc_dt = datetime(dt.year, dt.month, dt.day, tzinfo=ZoneInfo("UTC")) + timedelta(hours=UT)
    local_dt = utc_dt.astimezone(tz)

    return local_dt

# Entry point: calculate_sunset(dt: date, latitude: float, longitude: float, tz: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_84_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_sunset(dt, latitude, longitude, tz):
    result = calculate_sunset(dt, latitude, longitude, tz)
    formatted_result = format_value_dt(result, dt, latitude, longitude, tz)
    log_file.write(formatted_result + "\n")

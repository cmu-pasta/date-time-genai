
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_sidereal_time(dt: pendulum.DateTime, longitude: float) -> float:
    # Ensure the input datetime is in UTC for standard astronomical calculations
    dt_utc = dt.in_timezone('UTC')

    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour
    minute = dt_utc.minute
    second = dt_utc.second

    # Step 1: Calculate Julian Date (JD)
    # Adjust month and year for JD calculation if month is Jan or Feb
    if month <= 2:
        year -= 1
        month += 12

    # Calculate integer parts for JD formula
    A = int(year / 100)
    B = 2 - A + int(A / 4)

    # Julian Date (JD) formula
    jd = (
        int(365.25 * (year + 4716)) +
        int(30.6001 * (month + 1)) +
        day +
        B - 1524.5
    )

    # Add time of day to JD
    jd += (hour + minute / 60 + second / 3600) / 24

    # Step 2: Calculate Julian Centuries (T) from J2000.0 (JD 2451545.0)
    T = (jd - 2451545.0) / 36525.0

    # Step 3: Calculate Greenwich Mean Sidereal Time (GMST) in hours
    # Formula from Astronomical Almanac (approximate for GMST)
    gmst_hours = (
        6.697374558 +
        1.00273790935 * (jd - 2451545.0) +
        (0.000025862 * T * T)
    )

    # Normalize GMST to be within 0-24 hours
    gmst_hours = gmst_hours % 24
    if gmst_hours < 0:
        gmst_hours += 24

    # Step 4: Calculate Local Sidereal Time (LST)
    # LST = GMST + Longitude / 15 (longitude in degrees, LST in hours)
    lst_hours = gmst_hours + (longitude / 15.0)

    # Normalize LST to be within 0-24 hours
    lst_hours = lst_hours % 24
    if lst_hours < 0:
        lst_hours += 24

    return lst_hours

# Entry point: calculate_sidereal_time(dt: pendulum.DateTime, longitude: float) -> float

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_93_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude):
    result = calculate_sidereal_time(dt, longitude)
    formatted_result = format_value_pd(result, dt, longitude)
    log_file.write(formatted_result + "\n")

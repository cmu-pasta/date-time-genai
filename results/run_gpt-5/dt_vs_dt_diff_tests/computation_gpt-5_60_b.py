
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import math
def calculate_solar_noon(d: date, latitude: float, longitude: float, tz: ZoneInfo) -> datetime:
    """
    Calculate the local solar noon time for a given date and location.

    Inputs:
    - d: date (the calendar date for which to compute solar noon)
    - latitude: float (degrees; accepted but not required for solar noon time)
    - longitude: float (degrees East; West is negative)
    - tz: ZoneInfo (local time zone)

    Output:
    - datetime: timezone-aware datetime representing local solar noon on date d
    """
    # Day of year
    n = d.timetuple().tm_yday

    # Equation of Time (minutes), using a common approximation
    B = 2.0 * math.pi * (n - 81) / 364.0
    eot_minutes = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

    # Local Standard Time Meridian (degrees), derived from time zone offset on that date
    # LSTM = 15° * (UTC offset hours)
    local_noon_guess = datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=tz)
    utc_offset_hours = local_noon_guess.utcoffset().total_seconds() / 3600.0
    lstm_deg = 15.0 * utc_offset_hours

    # Time Correction (minutes): accounts for longitude difference and Equation of Time
    # Positive TC means solar time is ahead of local clock time
    time_correction_minutes = 4.0 * (longitude - lstm_deg) + eot_minutes

    # Local clock time of solar noon (hours)
    local_noon_hours = 12.0 - (time_correction_minutes / 60.0)

    # Construct the timezone-aware datetime for solar noon
    day_start = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=tz)
    solar_noon_dt = day_start + timedelta(hours=local_noon_hours)

    return solar_noon_dt

# Entry point: calculate_solar_noon(d: date, latitude: float, longitude: float, tz: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_60_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_solar_noon(d, latitude, longitude, tz):
    result = calculate_solar_noon(d, latitude, longitude, tz)
    formatted_result = format_value_dt(result, d, latitude, longitude, tz)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timedelta, time, timezone
def calculate_solar_noon_time(d: date, latitude: float, longitude: float) -> datetime:
    """
    Calculates an approximate solar noon time for a given date and location.
    This approximation primarily accounts for longitude and ignores the Equation of Time,
    which requires astronomical calculations beyond the scope of the standard datetime library.
    The result is returned in UTC.

    Args:
        d (date): The date for which to calculate solar noon.
        latitude (float): The latitude of the location (degrees). Not used in this simplified
                          calculation but included as per problem statement.
        longitude (float): The longitude of the location (degrees, positive for East, negative for West).

    Returns:
        datetime: The approximate solar noon time in UTC for the given date and longitude.
                  This datetime object will be timezone-aware (UTC).
    """
    # Step 1: Create a base UTC datetime object for noon on the given date.
    # We assume mean solar noon is roughly 12:00 PM UTC at the Prime Meridian (0 longitude).
    base_utc_noon = datetime.combine(d, time(12, 0, 0), tzinfo=timezone.utc)

    # Step 2: Calculate the time adjustment due to longitude.
    # The Earth rotates 15 degrees per hour, so 1 degree = 4 minutes.
    # Positive longitude (East) means solar noon occurs earlier in UTC.
    # Negative longitude (West) means solar noon occurs later in UTC.
    # So, we subtract for East longitude and add for West longitude.
    # Or simply: subtract (longitude * 4 minutes) from the base UTC noon.
    longitude_offset_minutes = longitude * 4
    
    # Create a timedelta for the longitude offset
    # A negative offset for positive longitude means it happens earlier UTC.
    # A positive offset for negative longitude means it happens later UTC.
    time_adjustment = timedelta(minutes=-longitude_offset_minutes)

    # Step 3: Apply the adjustment to find the approximate solar noon.
    solar_noon_utc = base_utc_noon + time_adjustment
    
    # Step 4: Return the result as a timezone-aware datetime object (UTC).
    return solar_noon_utc

# Entry point: calculate_solar_noon_time(d: date, latitude: float, longitude: float) -> datetime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_60_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_solar_noon_time(d, latitude, longitude):
    result = calculate_solar_noon_time(d, latitude, longitude)
    formatted_result = format_value_dt(result, d, latitude, longitude)
    log_file.write(formatted_result + "\n")

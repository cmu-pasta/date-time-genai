
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
def calculate_sidereal_time(dt_input: datetime, longitude: float) -> float:
    """
    Calculates the Local Mean Sidereal Time (LMST) for a given datetime and longitude.

    Args:
        dt_input: The input datetime object. It is recommended to provide this
                  in UTC or with timezone information. If it's naive, it's treated as UTC.
        longitude: The longitude in degrees. Positive for East, negative for West.

    Returns:
        The Local Mean Sidereal Time (LMST) in hours (0 to 24).
    """
    # Step 1 & 2: Define J2000.0 epoch and convert input datetime to UTC
    # J2000.0 epoch: 2000 January 1, 12:00:00 UT
    J2000_EPOCH = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    # Convert input datetime to UTC. If naive, assume it's already UTC.
    if dt_input.tzinfo is None:
        dt_utc = dt_input.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt_input.astimezone(timezone.utc)

    # Step 3: Calculate the number of Julian days since J2000.0
    # The difference in days, including fractional part.
    delta_t = dt_utc - J2000_EPOCH
    D = delta_t.total_seconds() / (24 * 3600.0) # Total days since J2000.0

    # Step 4: Calculate Greenwich Mean Sidereal Time (GMST) in degrees
    # T is the number of Julian centuries since J2000.0
    T = D / 36525.0

    # GMST formula (degrees) - from Explanatory Supplement to the Astronomical Almanac
    # and other standard astronomical sources.
    GMST_deg = (280.46061837 +
                360.98564736629 * D +
                0.000387933 * T**2 -
                T**3 / 38710000.0)

    # Normalize GMST to 0-360 degrees
    GMST_deg = GMST_deg % 360.0
    if GMST_deg < 0:
        GMST_deg += 360.0

    # Convert GMST from degrees to hours
    GMST_hours = GMST_deg / 15.0

    # Step 5: Calculate Local Mean Sidereal Time (LMST)
    # Convert longitude from degrees to hours (15 degrees = 1 hour)
    longitude_hours = longitude / 15.0

    LMST_hours = GMST_hours + longitude_hours

    # Step 6: Normalize the result to 0-24 hours
    LMST_hours = LMST_hours % 24.0
    if LMST_hours < 0:
        LMST_hours += 24.0

    return LMST_hours

# Entry point: calculate_sidereal_time(dt_input: datetime, longitude: float) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_93_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt_input, longitude):
    result = calculate_sidereal_time(dt_input, longitude)
    formatted_result = format_value_dt(result, dt_input, longitude)
    log_file.write(formatted_result + "\n")

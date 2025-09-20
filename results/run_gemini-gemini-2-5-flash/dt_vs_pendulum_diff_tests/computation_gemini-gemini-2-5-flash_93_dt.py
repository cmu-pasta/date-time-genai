
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
def calculate_sidereal_time(dt_utc: datetime, longitude_degrees: float) -> float:
    """
    Calculates the Local Sidereal Time (LST) for a given UTC datetime and longitude.

    This function attempts to adhere strictly to the 'datetime' library only
    constraint, which means it uses a simplified astronomical model and
    may not achieve the same precision as implementations using math or
    specialized astronomical libraries.

    Args:
        dt_utc: The datetime object in UTC.
        longitude_degrees: The longitude in degrees (east is positive).

    Returns:
        The Local Sidereal Time (LST) in hours (0.0 to 24.0).
    """
    # Step 1: Define a reference epoch (J2000.0, January 1, 2000, 12:00:00 UTC)
    # The sidereal time at J2000.0 (1 Jan 2000, 12:00:00 UT1) is 6.70044566 hours.
    # We will use UTC directly.
    j2000_epoch = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    # Step 2: Calculate the time difference from the reference epoch
    # Ensure dt_utc is timezone-aware. If not, assume it's UTC.
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)

    time_diff: timedelta = dt_utc - j2000_epoch

    # Step 3: Convert timedelta to fractional days
    # total_seconds() returns a float, so this should work without external math.
    days_since_epoch = time_diff.total_seconds() / (24 * 3600.0)

    # Step 4: Calculate Greenwich Mean Sidereal Time (GMST) in hours
    # Simplified formula (from various sources, e.g., 'Practical Astronomy with your Calculator or Spreadsheet' by Peter Duffett-Smith and Jonathan Zwart)
    # A common simplified formula for GMST (in hours) at a given fractional day 'D'
    # since J2000.0 epoch is approximately:
    # GMST = (6.70044566 + 0.06570982441908 * D) % 24
    # The 0.06570982441908 comes from 24 * (1.00273790935 - 1) / 365.25... roughly.
    # More simply, the rate of increase of GMST per solar day is 24.06570982441908 hours.
    # So, GMST_hours = (Initial_GMST_at_epoch + days_since_epoch * sidereal_rate_factor)
    
    # Initial GMST at J2000.0 (1 Jan 2000 12:00:00 UT1) in hours
    initial_gmst_at_j2000 = 6.70044566 
    
    # Sidereal rate factor (hours of sidereal time per solar day)
    # 1.00273790935 is the ratio of sidereal day to mean solar day
    sidereal_rate_factor = 24.0 * 1.00273790935 

    gmst_hours = initial_gmst_at_j2000 + (days_since_epoch * sidereal_rate_factor)
    
    # Step 5: Adjust for Longitude to get Local Sidereal Time (LST)
    # Longitude is in degrees, convert to hours (15 degrees = 1 hour)
    longitude_in_hours = longitude_degrees / 15.0

    lst_hours = gmst_hours + longitude_in_hours

    # Step 6: Normalize to 0-24 hours
    # Use modulo operator to keep the result in the 0-24 range
    lst_hours_normalized = lst_hours % 24.0
    
    # Handle negative results from modulo if lst_hours was very negative
    if lst_hours_normalized < 0:
        lst_hours_normalized += 24.0

    return lst_hours_normalized

# Entry point: calculate_sidereal_time(dt_utc: datetime, longitude_degrees: float) -> float

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_93_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt_utc, longitude_degrees):
    result = calculate_sidereal_time(dt_utc, longitude_degrees)
    formatted_result = format_value_dt(result, dt_utc, longitude_degrees)
    log_file.write(formatted_result + "\n")

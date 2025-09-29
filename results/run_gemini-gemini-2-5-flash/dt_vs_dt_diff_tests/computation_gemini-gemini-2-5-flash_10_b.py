
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_date_to_julian_day_number(dt: datetime) -> int:
    """
    Converts a datetime object to its Julian Day Number (JDN).

    The Julian Day Number is the integer part of the Julian Day.
    This function calculates the JDN for the date part of the datetime object
    at 0h UT (midnight).

    Args:
        dt: The datetime object to convert.

    Returns:
        The Julian Day Number as an integer.
    """
    year = dt.year
    month = dt.month
    day = dt.day

    # Adjust month and year for the formula if month is January or February
    if month <= 2:
        year -= 1
        month += 12

    # Calculate the Gregorian calendar correction term
    # This term (B) is only relevant for dates after October 15, 1582.
    # Python's datetime objects are typically post-Gregorian calendar,
    # and this formula implicitly handles that by its structure.
    A = year // 100
    B = 2 - A + (A // 4)

    # Calculate the Julian Day (JD) using a standard astronomical formula
    # This formula calculates the JD for 0h UT (midnight) of the given date.
    # The Julian Day Number (JDN) is simply the integer part of this JD.
    # Using float(day) to ensure floating point arithmetic for precision before int conversion.
    julian_day = (
        int(365.25 * (year + 4716)) +
        int(30.6001 * (month + 1)) +
        float(day) + B - 1524.5
    )

    # The Julian Day Number is the integer part of the Julian Day for 0h UT.
    return int(julian_day)

# Entry point: convert_date_to_julian_day_number(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_10_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_date_to_julian_day_number(dt):
    result = convert_date_to_julian_day_number(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

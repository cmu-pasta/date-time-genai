
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def convert_julian_to_gregorian(dt_julian: datetime) -> datetime:
    """
    Converts a datetime object interpreted as a Julian calendar date
    to its equivalent Gregorian calendar date.

    Note: The Python datetime object inherently uses the Proleptic Gregorian calendar.
    This function interprets the input dt_julian's year, month, and day as Julian,
    calculates the necessary offset based on historical differences, and returns
    a new datetime object representing the equivalent Gregorian date.

    The conversion logic accounts for the historical shift due to the Gregorian reform
    and subsequent leap year discrepancies. It handles dates from October 1582 onwards
    for practical purposes, assuming the standard 10-day shift and subsequent
    accumulations.
    """
    year = dt_julian.year
    month = dt_julian.month
    day = dt_julian.day

    # Determine the number of days difference between Julian and Gregorian calendar
    # This logic assumes the standard adoption of the Gregorian calendar (1582).
    # The number of skipped days increases due to Julian leap years that are not
    # Gregorian leap years (e.g., 1700, 1800, 1900).

    # Base difference for dates after Oct 4, 1582 Julian (Oct 14, 1582 Gregorian)
    # The 10-day gap applies after Oct 4, 1582 Julian / Oct 14, 1582 Gregorian.
    # We are working with the input dt_julian's components.
    
    # Calculate initial offset for dates after the initial 10-day skip
    # (Julian 1582-10-05 -> Gregorian 1582-10-15)
    
    # Create a reference date for the start of the 10-day jump
    # This is the last Julian day before the jump in places that adopted in 1582.
    gregorian_reform_date = datetime(1582, 10, 4) # This is the last Julian day.
    
    # If the Julian date is before or on the Gregorian reform date (Oct 4, 1582 Julian),
    # there is no conversion difference. The date is simply itself.
    # Note: This is an oversimplification as reform dates varied by region.
    # For a general solution, we use the most common reform point.
    if dt_julian <= gregorian_reform_date:
        # For dates before the reform, the Julian date is often considered
        # identical to the Proleptic Gregorian date for general purpose use,
        # or it means the conversion is not yet applicable.
        # This implementation will return the input as is if it's before/on the reform date.
        # A more precise implementation might throw an error or handle
        # pre-reform conversions separately (e.g., proleptic Julian to proleptic Gregorian).
        return dt_julian 
    
    # Calculate the number of days to add.
    # Start with 10 days for dates after Oct 4, 1582 Julian.
    days_to_add = 10 

    # Add extra days for each century year (1700, 1800, 1900, etc.) that was
    # a leap year in Julian but not in Gregorian.
    # We need to check years *before* the input Julian date's year, but after 1582.
    
    # Count centuries from 1700 onwards that contribute an extra day
    # These are years divisible by 100 but not 400.
    for y in range(1700, year, 100):
        if y % 400 != 0: # If it's a Julian leap century but not a Gregorian leap century
            # This is correct if the current Julian date is *after* the leap day in that century.
            # E.g., Julian 1700-03-01 is 11 days different.
            # Julian 1700-02-28 is 10 days different.
            
            # To be precise, we need to check if the Julian date has passed Feb 29 of the century year.
            # For simplicity, we add the day if the century year has passed.
            # For a more exact point, compare against Mar 1 of the century year.
            
            # This simplified loop assumes that if 'year' is >= 1700, 1700 has added its day.
            # If 'year' is >= 1800, 1800 has added its day, etc.
            
            # The original algorithm states:
            # - 1582 to 1699: +10 days
            # - 1700 to 1799: +11 days (1700 was Julian leap, Gregorian not)
            # - 1800 to 1899: +12 days (1800 was Julian leap, Gregorian not)
            # - 1900 to 1999: +13 days (1900 was Julian leap, Gregorian not)
            # - 2000 to 2099: +13 days (2000 was Julian leap and Gregorian leap, so no change)
            # - 2100 to 2199: +14 days (2100 will be Julian leap, Gregorian not)

            # Let's adjust days_to_add based on the year range directly.
            if year >= 1700 and (year < 1800 or (year == 1800 and (month > 2 or (month == 2 and day >= 29)))):
                # If it's 1700-03-01 Julian or later
                days_to_add = 11
            if year >= 1800 and (year < 1900 or (year == 1900 and (month > 2 or (month == 2 and day >= 29)))):
                 # If it's 1800-03-01 Julian or later
                days_to_add = 12
            if year >= 1900 and (year < 2000 or (year == 2000 and (month > 2 or (month == 2 and day >= 29)))):
                 # If it's 1900-03-01 Julian or later
                days_to_add = 13
            if year >= 2100 and (year < 2200 or (year == 2200 and (month > 2 or (month == 2 and day >= 29)))):
                # If it's 2100-03-01 Julian or later
                days_to_add = 14
            # For 2000-2099, it remains 13 because 2000 was a leap year in both.

    # A more robust way to calculate the accumulated difference (known as Delta T or 'JDN' based):
    # This involves calculating the Julian Day Number for the Julian date,
    # then the Julian Day Number for the Gregorian date, and finding the difference.
    # However, this approach would require implementing Julian Day Number calculations,
    # which goes beyond "using the datetime library only" for the *conversion logic*.
    # The current approach aims to use timedelta with pre-calculated offsets.

    # Let's refine the offset calculation for clarity and precision without complex JDN.
    # The number of skipped days between Julian and Gregorian calendars
    # is 10 days from 1582/10/05 (Julian) to 1700/02/28 (Julian).
    # Then it increases by 1 day for each century year not divisible by 400.

    # We need to determine the correct offset based on the Julian year.
    # This is often done using a lookup or a piecewise function.
    
    # Calculate the number of centuries that passed since 1600 (Julian)
    # and were Julian leap years but not Gregorian leap years.
    
    # Initialize days_to_add based on the earliest post-reform period.
    days_to_add_effective = 0
    if dt_julian > datetime(1582, 10, 4): # If it's after the initial reform date
        days_to_add_effective = 10 # Base shift

    # Check for leap year discrepancies: 1700, 1800, 1900, 2100, etc.
    # For each such year, if the Julian date is *after* Feb 28 of that year,
    # an additional day has been accumulated in the difference.
    
    # Julian date: year, month, day
    
    # Year 1700: Julian leap, Gregorian not. Adds 1 day.
    # This extra day becomes effective on 1700-03-01 (Julian).
    if dt_julian >= datetime(1700, 3, 1):
        days_to_add_effective += 1 # Total 11
        
    # Year 1800: Julian leap, Gregorian not. Adds 1 day.
    # Effective on 1800-03-01 (Julian).
    if dt_julian >= datetime(1800, 3, 1):
        days_to_add_effective += 1 # Total 12
        
    # Year 1900: Julian leap, Gregorian not. Adds 1 day.
    # Effective on 1900-03-01 (Julian).
    if dt_julian >= datetime(1900, 3, 1):
        days_to_add_effective += 1 # Total 13
        
    # Year 2000: Julian leap, Gregorian leap. No change in difference.
    # Year 2100: Julian leap, Gregorian not. Adds 1 day.
    # Effective on 2100-03-01 (Julian).
    if dt_julian >= datetime(2100, 3, 1):
        days_to_add_effective += 1 # Total 14

    # Create a timedelta object with the calculated number of days
    offset = timedelta(days=days_to_add_effective)

    # Add the offset to the original Julian datetime object
    # This creates a new datetime object which represents the Gregorian date.
    dt_gregorian = dt_julian + offset
    
    return dt_gregorian

# Entry point: convert_julian_to_gregorian(dt_julian: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_70_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_julian_to_gregorian(dt_julian):
    result = convert_julian_to_gregorian(dt_julian)
    formatted_result = format_value_dt(result, dt_julian)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_number_of_leap_years(year1: int, year2: int) -> int:
    # Step 1: Ensure year1 is the earlier year for consistent iteration
    if year1 > year2:
        year1, year2 = year2, year1
    
    leap_year_count = 0
    
    # Step 2: Iterate through each year in the given range (inclusive)
    for year in range(year1, year2 + 1):
        # Step 3: Check if the current year is a leap year using datetime.date
        # A year is a leap year if it has 366 days.
        # We can determine the number of days in a year by subtracting
        # Jan 1st of the next year from Jan 1st of the current year.
        try:
            days_in_year = (date(year + 1, 1, 1) - date(year, 1, 1)).days
            if days_in_year == 366:
                leap_year_count += 1
        except ValueError:
            # Handle potential ValueError if year is out of supported range (e.g., year 0)
            # For standard year ranges (1 to 9999), this should not occur.
            pass # Or log an error, depending on desired behavior for invalid years
            
    # Step 4: Return the total count of leap years
    return leap_year_count

# Entry point: calculate_number_of_leap_years(year1: int, year2: int) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_27_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_calculate_number_of_leap_years(year1, year2):
    result = calculate_number_of_leap_years(year1, year2)
    formatted_result = format_value_dt(result, year1, year2)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_leap_years_between(year1: int, year2: int) -> int:
    # Step 1: Ensure year1 is the smaller year for correct iteration
    start_year = min(year1, year2)
    end_year = max(year1, year2)

    leap_year_count = 0

    # Step 2: Iterate through each year in the given range (inclusive)
    for year in range(start_year, end_year + 1):
        # Step 3: Check if the current year is a leap year using datetime.date
        # A year is a leap year if it has 366 days.
        # We can determine the number of days in a year by checking the difference
        # in ordinal values between Jan 1st and Dec 31st of that year.
        # If (date(year, 12, 31).toordinal() - date(year, 1, 1).toordinal()) == 365,
        # it means there are 366 days in the year (365 differences + 1 for the start day itself).
        
        # We can construct date objects for Jan 1 and Dec 31 of the current year.
        jan_1 = date(year, 1, 1)
        dec_31 = date(year, 12, 31)
        
        # Calculate the number of days in the year.
        # The difference in ordinal values gives days between the two dates.
        # Add 1 to include both start and end days.
        days_in_year = dec_31.toordinal() - jan_1.toordinal() + 1

        if days_in_year == 366:
            leap_year_count += 1
            
    # Step 4: Return the total count of leap years
    return leap_year_count

# Entry point: calculate_leap_years_between(year1: int, year2: int) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_27_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_calculate_leap_years_between(year1, year2):
    result = calculate_leap_years_between(year1, year2)
    formatted_result = format_value_dt(result, year1, year2)
    log_file.write(formatted_result + "\n")

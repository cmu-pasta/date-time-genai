
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_easter_sunday(year: int) -> date:
    # Algorithm for calculating Easter Sunday based on the Gregorian calendar
    # This uses the algorithm commonly known as the "Anonymous Gregorian algorithm"
    
    # Calculate the golden number (19-year Metonic cycle)
    golden = (year % 19) + 1
    
    # Calculate the century
    century = (year // 100) + 1
    
    # Calculate leap year corrections
    leap_correction = (3 * century) // 4 - 12
    moon_correction = (8 * century + 5) // 25 - 5
    
    # Calculate the Sunday letter (day of week for January 1st)
    sunday_letter = (5 * year) // 4 - leap_correction - 10
    
    # Calculate the epact (age of moon on January 1st)
    epact = (11 * golden + 20 + moon_correction - leap_correction) % 30
    
    # Adjust epact for specific cases
    if (epact == 25 and golden > 11) or epact == 24:
        epact += 1
    
    # Calculate the paschal full moon date in March
    full_moon_date = 44 - epact
    if full_moon_date < 21:
        full_moon_date += 30
    
    # Find the first Sunday after the paschal full moon
    easter_date = full_moon_date + 7 - ((sunday_letter + full_moon_date) % 7)
    
    # Determine the month and day
    if easter_date > 31:
        # Easter falls in April
        return date(year, 4, easter_date - 31)
    else:
        # Easter falls in March
        return date(year, 3, easter_date)

# Entry point: find_easter_sunday(year: int) -> date

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_11txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_easter_sunday(year):
    result = find_easter_sunday(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

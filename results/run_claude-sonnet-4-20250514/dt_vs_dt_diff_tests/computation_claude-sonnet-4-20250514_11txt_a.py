
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_easter_sunday(year: int) -> date:
    # Easter calculation algorithm for Western Christianity (Gregorian calendar)
    
    # Step 1: Calculate the Golden Number
    golden_number = year % 19 + 1
    
    # Step 2: Calculate the century
    century = year // 100 + 1
    
    # Step 3: Calculate corrections
    correction_x = (3 * century) // 4 - 12
    correction_z = (8 * century + 5) // 25 - 5
    
    # Step 4: Calculate Sunday letter correction
    sunday_correction = (5 * year) // 4 - correction_x - 10
    
    # Step 5: Calculate the epact (age of moon on Jan 1)
    epact = (11 * golden_number + 20 + correction_z - correction_x) % 30
    if (epact == 25 and golden_number > 11) or epact == 24:
        epact += 1
    
    # Step 6: Find the full moon date
    full_moon_day = 44 - epact
    if full_moon_day < 21:
        full_moon_day += 30
    
    # Step 7: Find the Sunday after the full moon
    full_moon_day = full_moon_day + 7 - ((sunday_correction + full_moon_day) % 7)
    
    # Step 8: Determine if Easter is in March or April
    if full_moon_day > 31:
        # Easter is in April
        easter_month = 4
        easter_day = full_moon_day - 31
    else:
        # Easter is in March
        easter_month = 3
        easter_day = full_moon_day
    
    # Step 9: Return the Easter date
    return date(year, easter_month, easter_day)

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_11txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_easter_sunday(year):
    result = find_easter_sunday(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def orthodox_easter(year: int) -> date:
    """
    Calculates the date of Orthodox Easter for a given year in the Gregorian calendar.
    
    :param year: The year as an integer.
    :return: The date of Orthodox Easter as a datetime.date object.
    """
    # Step 1: Calculate intermediate values for the Julian calendar
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = ((d + e + 114) // 31)
    day = ((d + e + 114) % 31) + 1
    
    # Step 2: Get the Julian Easter date
    julian_easter = date(year, month, day)
    
    # Step 3: Calculate days difference between Julian and Gregorian calendars in the 20th-21st century
    # For years 1900–2099, the difference is 13 days.
    # For years 2100–2199, the difference is 14 days.
    # (General formula: 13 + (year >= 2100))
    if 1900 <= year <= 2099:
        diff = 13
    elif 2100 <= year <= 2199:
        diff = 14
    else:
        # Generalized calculation using Gregorian reform offset
        diff = (year // 100) - (year // 400) - 2
    
    # Step 4: Convert Julian Easter to Gregorian Easter
    orthodox_easter_date = julian_easter.toordinal() + diff
    gregorian_easter = date.fromordinal(orthodox_easter_date)
    
    # Step 5: Return the computed Gregorian date of Orthodox Easter
    return gregorian_easter

# Entry point: orthodox_easter(year: int) -> date

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_70txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_orthodox_easter(year):
    result = orthodox_easter(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

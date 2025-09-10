
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def orthodox_easter(year: int) -> date:
    """
    Calculate the date of Orthodox Easter (Pascha) for a given year.
    The computation uses the Julian calendar and converts the result to the Gregorian calendar.
    """

    # Step 1: Compute the Julian Easter date using the Meeus Julian algorithm
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = 3  # March
    day = d + e + 114

    # The Julian Easter is (day // 31) is the month (either March or April), day % 31 + 1 is the day
    julian_month = day // 31
    julian_day = (day % 31) + 1

    # Julian date of Easter Sunday
    julian_easter = date(year, julian_month, julian_day)

    # Step 2: Calculate the difference between Julian and Gregorian calendars for the given year
    # Formula for Gregorian difference (valid for years >= 1583)
    gregorian_shift = year // 100 - year // 400 - 2

    # Step 3: Convert Julian date to Gregorian date by adding the shift
    gregorian_easter = julian_easter + timedelta(days=gregorian_shift)

    # Step 4: Return the Gregorian date
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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_70txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_orthodox_easter(year):
    result = orthodox_easter(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

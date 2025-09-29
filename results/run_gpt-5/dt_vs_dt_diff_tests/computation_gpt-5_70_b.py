
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def julian_to_gregorian(year: int, month: int, day: int) -> date:
    """
    Convert a Julian calendar date (year, month, day) to a Gregorian calendar date.
    Returns a datetime.date in the proleptic Gregorian calendar.
    """

    # Convert Julian calendar date to Julian Day Number (JDN)
    # Algorithm valid for all Julian calendar dates
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + ((153 * m + 2) // 5) + 365 * y + (y // 4) - 32083

    # Convert JDN to Gregorian date (proleptic Gregorian calendar)
    a = jdn + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153

    day_g = e - (153 * m + 2) // 5 + 1
    month_g = m + 3 - 12 * (m // 10)
    year_g = 100 * b + d - 4800 + (m // 10)

    # Construct and return the Gregorian date
    return date(year_g, month_g, day_g)

# Entry point: julian_to_gregorian(year: int, month: int, day: int) -> date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_70_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_julian_to_gregorian(year, month, day):
    result = julian_to_gregorian(year, month, day)
    formatted_result = format_value_dt(result, year, month, day)
    log_file.write(formatted_result + "\n")

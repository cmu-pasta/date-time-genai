
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def convert_julian_to_gregorian(year: int, month: int, day: int) -> date:
    """
    Convert a Julian calendar date to a Gregorian calendar date.

    Parameters:
    - year: int  (Julian calendar year)
    - month: int (1-12, Julian calendar)
    - day: int   (1-31, Julian calendar)

    Returns:
    - datetime.date corresponding to the same absolute day in the Gregorian calendar.
    """
    # Step 1: Convert the Julian calendar date to Julian Day Number (JDN)
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083

    # Step 2: Convert JDN to Gregorian date (proleptic Gregorian calendar)
    A = jdn + 32044
    B = (4 * A + 3) // 146097
    C = A - (146097 * B) // 4
    D = (4 * C + 3) // 1461
    E = C - (1461 * D) // 4
    M = (5 * E + 2) // 153

    g_day = E - (153 * M + 2) // 5 + 1
    g_month = M + 3 - 12 * (M // 10)
    g_year = 100 * B + D - 4800 + (M // 10)

    # Step 3: Construct and return the Gregorian date
    return date(g_year, g_month, g_day)

# Entry point: convert_julian_to_gregorian(year: int, month: int, day: int) -> date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_70_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_convert_julian_to_gregorian(year, month, day):
    result = convert_julian_to_gregorian(year, month, day)
    formatted_result = format_value_dt(result, year, month, day)
    log_file.write(formatted_result + "\n")

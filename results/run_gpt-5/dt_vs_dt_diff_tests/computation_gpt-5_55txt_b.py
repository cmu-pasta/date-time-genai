
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _gregorian_to_jdn(g_year: int, g_month: int, g_day: int) -> int:
    """
    Convert a Gregorian date to Julian Day Number (JDN).
    Uses the proleptic Gregorian calendar for all dates.
    """
    a = (14 - g_month) // 12
    y = g_year + 4800 - a
    m = g_month + 12 * a - 3
    # Integer JDN for 0h UTC of the Gregorian date
    jdn = g_day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return jdn

def _jdn_to_islamic_civil(jdn: int) -> (int, int, int):
    """
    Convert Julian Day Number (JDN) to Islamic (Hijri, civil/arithmetic) date.
    Returns (year, month, day) using an integer-only algorithm.
    """
    # This algorithm corresponds to the widely used arithmetic Hijri calendar.
    l = jdn - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    m = (24 * l) // 709
    d = l - (709 * m) // 24
    y = 30 * n + j - 30
    return y, m, d

def gregorian_to_islamic(g_date: date) -> date:
    """
    Convert a Gregorian date to its Islamic (Hijri civil) date.
    Input:  g_date (datetime.date) - Gregorian calendar date.
    Output: datetime.date where year, month, day correspond to the Islamic (Hijri civil) date.
    """
    jdn = _gregorian_to_jdn(g_date.year, g_date.month, g_date.day)
    h_year, h_month, h_day = _jdn_to_islamic_civil(jdn)
    # Return the Hijri date encoded in a datetime.date object
    return date(h_year, h_month, h_day)

# Entry point: gregorian_to_islamic(g_date: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_55txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_islamic(g_date):
    result = gregorian_to_islamic(g_date)
    formatted_result = format_value_dt(result, g_date)
    log_file.write(formatted_result + "\n")

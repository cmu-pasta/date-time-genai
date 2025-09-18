
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _gregorian_to_jdn(g_date: date) -> int:
    # Convert a Gregorian date to Julian Day Number (JDN)
    y = g_date.year
    m = g_date.month
    d = g_date.day
    a = (14 - m) // 12
    y_prime = y + 4800 - a
    m_prime = m + 12 * a - 3
    jdn = d + (153 * m_prime + 2) // 5 + 365 * y_prime + y_prime // 4 - y_prime // 100 + y_prime // 400 - 32045
    return jdn

def _jdn_to_islamic_ymd(jdn: int) -> (int, int, int):
    # Convert JDN to Islamic (Hijri) date using the tabular Islamic calendar (civil)
    # This is a well-known integer arithmetic algorithm.
    l = jdn - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    m = (24 * l) // 709
    d = l - (709 * m) // 24
    y = 30 * n + j - 30
    return y, m, d

def gregorian_to_islamic_yyyymmdd(gregorian_date: date) -> int:
    """
    Convert a Gregorian date to an Islamic (Hijri) date and return it as an integer YYYYMMDD.
    Uses the tabular (civil) Islamic calendar.
    """
    jdn = _gregorian_to_jdn(gregorian_date)
    y, m, d = _jdn_to_islamic_ymd(jdn)
    # Encode as a single integer to satisfy allowed output types
    return y * 10000 + m * 100 + d

# Entry point: gregorian_to_islamic_yyyymmdd(gregorian_date: date) -> int

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_55txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_islamic_yyyymmdd(gregorian_date):
    result = gregorian_to_islamic_yyyymmdd(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")

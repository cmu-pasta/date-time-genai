
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
# Julian Day Number (JDN) from Gregorian date (valid for proleptic Gregorian calendar)
def _gregorian_to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    # Integer JDN (days start at noon; this standard formula yields an integer JDN)
    return d + ((153 * m2 + 2) // 5) + 365 * y2 + (y2 // 4) - (y2 // 100) + (y2 // 400) - 32045

# Islamic (civil/tabular) calendar constants and conversions
_ISLAMIC_EPOCH_JDN = 1948439  # JDN of 1 Muharram, year 1 (civil Islamic epoch), integer-based

def _islamic_to_jdn(y: int, m: int, d: int) -> int:
    # Arithmetic Islamic calendar: 354-day common years, leap in 11 of every 30 years
    # Month lengths alternate 30/29 with Dhul-Hijjah 30 in leap years.
    # Using standard tabular formula with average month length 29.5 via ceil.
    # ceil(29.5 * (m - 1)) = ceil((59 * (m - 1)) / 2) = ((59 * (m - 1)) + 1) // 2
    months_elapsed_ceiling = ((59 * (m - 1)) + 1) // 2
    leap_days = (3 + 11 * y) // 30
    return d + months_elapsed_ceiling + (y - 1) * 354 + leap_days + _ISLAMIC_EPOCH_JDN - 1

def _jdn_to_islamic(jdn: int) -> date:
    # Compute Islamic year using closed-form approximation
    y = (30 * (jdn - _ISLAMIC_EPOCH_JDN) + 10646) // 10631

    # Estimate month: m = min(12, ceil((jdn - 29 - islamic_to_jdn(y,1,1)) / 29.5) + 1)
    # Implement ceil division by 29.5 as ceil(2*x / 59) = (2*x + 58) // 59
    jdn_y1m1 = _islamic_to_jdn(y, 1, 1)
    t = jdn - 29 - jdn_y1m1
    m = (2 * t + 58) // 59 + 1
    if m > 12:
        m = 12
    if m < 1:
        m = 1

    # Day is the offset from the first day of the month
    d = jdn - _islamic_to_jdn(y, m, 1) + 1

    # Construct a date object with Islamic Y-M-D values
    return date(y, m, d)

def gregorian_to_islamic(gregorian_day: date) -> date:
    """
    Convert a Gregorian date to its Islamic (Hijri) civil calendar date.
    Inputs and outputs are datetime.date instances.
    The returned date's year, month, and day correspond to Islamic calendar values.
    """
    jdn = _gregorian_to_jdn(gregorian_day.year, gregorian_day.month, gregorian_day.day)
    return _jdn_to_islamic(jdn)

# Entry point: gregorian_to_islamic(gregorian_day: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_55_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_islamic(gregorian_day):
    result = gregorian_to_islamic(gregorian_day)
    formatted_result = format_value_dt(result, gregorian_day)
    log_file.write(formatted_result + "\n")

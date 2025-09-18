
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _div(a: int, b: int) -> int:
    # Integer division matching floor for non-negative b
    return a // b

def _mod(a: int, b: int) -> int:
    return a % b

def _jalCal(jy: int) -> (int, int):
    # Calculates Gregorian year (gy) and March day (march) for the start of Jalaali year jy.
    # This is based on the well-known Jalaali calendar arithmetic with defined break points.
    breaks = [
        -61, 9, 38, 199, 426, 686, 756, 818, 1111,
        1181, 1210, 1635, 2060, 2097, 2192, 2262,
        2324, 2394, 2456, 3178
    ]
    gy = jy + 621
    leapJ = -14
    jp = breaks[0]
    jump = 0

    # Advance through break points to find the segment containing jy
    for jm in breaks[1:]:
        jump = jm - jp
        if jy < jm:
            break
        leapJ += _div(jump, 33) * 8 + _div(_mod(jump, 33), 4)
        jp = jm

    N = jy - jp
    leapJ += _div(N, 33) * 8 + _div(_mod(N, 33) + 3, 4)
    if _mod(jump, 33) == 4 and (jump - N) == 4:
        leapJ += 1

    leapG = _div(gy, 4) - _div((_div(gy, 100) + 1) * 3, 4) - 150
    march = 20 + leapJ - leapG

    return gy, march

def persian_new_year_date(gregorian_year: int) -> date:
    """
    Return the Gregorian date of Persian New Year (Nowruz) for the given Gregorian year.
    The result is the date in March on which 1 Farvardin occurs in that Gregorian year.
    """
    jy = gregorian_year - 621
    gy, march_day = _jalCal(jy)
    # gy should equal gregorian_year; march_day is the day in March when Nowruz occurs.
    return date(gy, 3, march_day)

# Entry point: persian_new_year_date(gregorian_year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_89txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_persian_new_year_date(gregorian_year):
    result = persian_new_year_date(gregorian_year)
    formatted_result = format_value_dt(result, gregorian_year)
    log_file.write(formatted_result + "\n")

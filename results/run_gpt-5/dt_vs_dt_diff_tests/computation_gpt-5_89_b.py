
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def _jalali_calendar_march_and_leap(jy: int):
    # Jalaali calendar leap year and March day calculation based on the "breaks" method.
    # Returns (is_leap_year, march_day_in_gregorian_year)
    breaks = (-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181,
              1210, 1635, 2060, 2097, 2192, 2262, 2324, 2394,
              2456, 3178)

    gy = jy + 621
    leap_j = -14
    jp = breaks[0]

    for jm in breaks[1:]:
        jump = jm - jp
        if jy < jm:
            break
        leap_j += (jump // 33) * 8 + ((jump % 33) // 4)
        jp = jm
    else:
        jump = breaks[-1] - jp  # for completeness

    n = jy - jp
    leap_j += (n // 33) * 8 + ((n % 33 + 3) // 4)

    if (jump % 33 == 4) and (jump - n == 4):
        leap_j += 1

    leap_g = gy // 4 - ((gy // 100 + 1) * 3 // 4) - 150
    march = 20 + leap_j - leap_g

    if (jump - n) == 1:
        is_leap = False
    else:
        if (n % 33) == 4 and (jump - n) != 4:
            is_leap = True
        else:
            is_leap = ((n + 1) % 33) % 4 == 0

    return is_leap, march

def _jalali_to_gregorian(jy: int, jm: int, jd: int) -> date:
    # Convert a Jalaali (Persian) date to Gregorian date using the computed March anchor.
    _, march = _jalali_calendar_march_and_leap(jy)
    gy = jy + 621

    if jm <= 7:
        days = (jm - 1) * 31 + (jd - 1)
    else:
        days = 6 * 31 + (jm - 7 - 1) * 30 + (jd - 1)

    anchor = date(gy, 3, march)
    return anchor + timedelta(days=days)

def find_nowruz(gregorian_year: int) -> date:
    # For a given Gregorian year, Nowruz is Farvardin 1 of the Jalaali year (gregorian_year - 621).
    jy = gregorian_year - 621
    return _jalali_to_gregorian(jy, 1, 1)

# Entry point: find_nowruz(gregorian_year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_89_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_nowruz(gregorian_year):
    result = find_nowruz(gregorian_year)
    formatted_result = format_value_dt(result, gregorian_year)
    log_file.write(formatted_result + "\n")

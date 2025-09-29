
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _march_day_for_jalali_year(jy: int) -> int:
    # Arithmetic Jalali calendar parameters (break points)
    breaks = [-61, 9, 38, 199, 426, 686, 756, 818,
              1111, 1181, 1210, 1635, 2060, 2097,
              2192, 2262, 2324, 2394, 2456, 3178]

    gy = jy + 621
    leap_j = -14
    jp = breaks[0]

    for jm in breaks[1:]:
        jump = jm - jp
        if jy < jm:
            n = jy - jp
            leap_j += (n // 33) * 8 + ((n % 33 + 3) // 4)
            # Special correction
            if (jump % 33 == 4) and (jump - n == 4):
                leap_j += 1
            leap_g = (gy // 4) - ((gy // 100 + 1) // 25) + (gy // 400)
            march = 20 + leap_j - leap_g
            return march
        leap_j += (jump // 33) * 8 + ((jump % 33) // 4)
        jp = jm

    # For years beyond the last break
    n = jy - jp
    leap_j += (n // 33) * 8 + ((n % 33 + 3) // 4)
    leap_g = (gy // 4) - ((gy // 100 + 1) // 25) + (gy // 400)
    march = 20 + leap_j - leap_g
    return march

def nowruz_date_for_gregorian_year(year: int) -> date:
    # Convert Gregorian year to Jalali year
    jy = year - 621
    # Compute the day in March when Nowruz occurs
    march_day = _march_day_for_jalali_year(jy)
    # Return the Gregorian date of Nowruz
    return date(year, 3, march_day)

# Entry point: nowruz_date_for_gregorian_year(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_89_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_nowruz_date_for_gregorian_year(year):
    result = nowruz_date_for_gregorian_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
# Internal constants for the Islamic civil calendar
_ISLAMIC_EPOCH_JDN = 1948439  # JDN for 1 Muharram, year 1 (civil/tabular algorithm)

def _gregorian_to_jdn(y: int, m: int, d: int) -> int:
    # Gregorian date to Julian Day Number (JDN), valid for proleptic Gregorian calendar
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045

def _islamic_to_jdn(y: int, m: int, d: int) -> int:
    # Islamic civil date to JDN using integer arithmetic
    # ceil(29.5*(m-1)) == (59*(m-1) + 1) // 2
    month_days = (59 * (m - 1) + 1) // 2
    leap_days = (3 + 11 * y) // 30
    return d + month_days + (y - 1) * 354 + leap_days + _ISLAMIC_EPOCH_JDN - 1

def gregorian_to_islamic_date(greg: date) -> date:
    # Step 1: Convert Gregorian date to JDN
    jdn = _gregorian_to_jdn(greg.year, greg.month, greg.day)

    # Step 2: Estimate Islamic year from JDN
    days_since_epoch = jdn - _ISLAMIC_EPOCH_JDN
    islamic_year = (30 * days_since_epoch + 10646) // 10631  # floor

    # Step 3: Find Islamic month by estimating then refining
    start_of_year_jdn = _islamic_to_jdn(islamic_year, 1, 1)
    r = jdn - start_of_year_jdn + 1  # day-of-year starting at 1

    # Estimate month via ceil(r / 29.5) with integer arithmetic: ceil(2r / 59)
    est_month = (2 * r + 59 - 1) // 59
    if est_month < 1:
        est_month = 1
    if est_month > 12:
        est_month = 12

    # Refine by ensuring the month start is <= jdn and next month start is > jdn
    # Adjust downward if needed
    while est_month > 1 and _islamic_to_jdn(islamic_year, est_month, 1) > jdn:
        est_month -= 1
    # Adjust upward if needed
    while est_month < 12 and _islamic_to_jdn(islamic_year, est_month + 1, 1) <= jdn:
        est_month += 1

    islamic_month = est_month

    # Step 4: Compute Islamic day
    start_of_month_jdn = _islamic_to_jdn(islamic_year, islamic_month, 1)
    islamic_day = jdn - start_of_month_jdn + 1

    # Step 5: Return as a date object whose Y-M-D fields represent the Islamic date
    return date(islamic_year, islamic_month, islamic_day)

# Entry point: gregorian_to_islamic_date(greg: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_55_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_islamic_date(greg):
    result = gregorian_to_islamic_date(greg)
    formatted_result = format_value_dt(result, greg)
    log_file.write(formatted_result + "\n")

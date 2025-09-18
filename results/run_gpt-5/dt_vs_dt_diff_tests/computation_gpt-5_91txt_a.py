
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _is_gregorian_leap(year: int) -> bool:
    """Return True if the Gregorian year is a leap year."""
    return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)

def gregorian_to_indian_national_calendar(gregorian_day: date) -> date:
    """
    Convert a Gregorian date to the Indian National Calendar (Saka) date.
    
    Returns a date object where:
      - year = Saka year
      - month = Saka month (1=Chaitra, ..., 12=Phalguna)
      - day = day of Saka month (1-based)
    """
    gy = gregorian_day.year

    # Determine Saka new year start date for the Gregorian year
    start_month = 3  # March
    start_day_current = 21 if _is_gregorian_leap(gy) else 22
    saka_start_current = date(gy, start_month, start_day_current)

    if gregorian_day >= saka_start_current:
        saka_year = gy - 78
        saka_start_greg_year = gy
        saka_start_date = saka_start_current
    else:
        prev_gy = gy - 1
        start_day_prev = 21 if _is_gregorian_leap(prev_gy) else 22
        saka_start_date = date(prev_gy, start_month, start_day_prev)
        saka_start_greg_year = prev_gy
        saka_year = gy - 79

    # Chaitra length depends on whether the Saka year started in a Gregorian leap year
    chaitra_length = 31 if _is_gregorian_leap(saka_start_greg_year) else 30

    # Month lengths in Saka calendar starting from Chaitra
    month_lengths = (
        chaitra_length,  # Chaitra
        31, 31, 31, 31, 31,  # Vaisakha..Bhadra
        30, 30, 30, 30, 30, 30  # Ashwin..Phalguna
    )

    # Compute offset in days from Saka new year start
    delta_days = (gregorian_day - saka_start_date).days  # zero-based

    # Map offset into month and day
    month = 1
    remaining = delta_days
    for mlen in month_lengths:
        if remaining < mlen:
            day = remaining + 1
            break
        remaining -= mlen
        month += 1

    # Return a date object encoding the Saka Y-M-D
    return date(saka_year, month, day)

# Entry point: gregorian_to_indian_national_calendar(gregorian_day: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_91txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_indian_national_calendar(gregorian_day):
    result = gregorian_to_indian_national_calendar(gregorian_day)
    formatted_result = format_value_dt(result, gregorian_day)
    log_file.write(formatted_result + "\n")

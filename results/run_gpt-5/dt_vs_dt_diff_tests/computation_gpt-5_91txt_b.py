
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _is_gregorian_leap(year: int) -> bool:
    # Gregorian leap year rule
    return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)

def _chaitra_start_gregorian(g_year: int) -> date:
    # Chaitra 1 falls on March 22 in common years and March 21 in Gregorian leap years
    if _is_gregorian_leap(g_year):
        return date(g_year, 3, 21)
    else:
        return date(g_year, 3, 22)

def determine_indian_national_date(gregorian_day: date) -> date:
    # Determine which Gregorian year’s Chaitra 1 anchors this Saka year
    chaitra_start_this_year = _chaitra_start_gregorian(gregorian_day.year)
    if gregorian_day >= chaitra_start_this_year:
        saka_year = gregorian_day.year - 78
        chaitra_anchor = chaitra_start_this_year
        leap_for_chaitra = _is_gregorian_leap(gregorian_day.year)
    else:
        prev_year = gregorian_day.year - 1
        saka_year = prev_year - 78
        chaitra_anchor = _chaitra_start_gregorian(prev_year)
        leap_for_chaitra = _is_gregorian_leap(prev_year)

    # Month lengths in Saka year starting at Chaitra
    # Chaitra length depends on leap_for_chaitra
    chaitra_len = 31 if leap_for_chaitra else 30
    month_lengths = (
        chaitra_len,  # Chaitra
        31, 31, 31, 31, 31,  # Vaisakha .. Bhadra
        30, 30, 30, 30, 30, 30  # Asvina .. Phalguna
    )

    # Compute offset from Chaitra 1
    days_since_chaitra1 = (gregorian_day - chaitra_anchor).days

    # Determine Saka month and day
    month = 1
    remaining = days_since_chaitra1
    for ml in month_lengths:
        if remaining < ml:
            day = remaining + 1
            break
        remaining -= ml
        month += 1

    # Construct Saka calendar date as a standard date object
    # Note: The returned date's year/month/day represent Saka values.
    return date(saka_year, month, day)

# Entry point: determine_indian_national_date(gregorian_day: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_91txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_indian_national_date(gregorian_day):
    result = determine_indian_national_date(gregorian_day)
    formatted_result = format_value_dt(result, gregorian_day)
    log_file.write(formatted_result + "\n")

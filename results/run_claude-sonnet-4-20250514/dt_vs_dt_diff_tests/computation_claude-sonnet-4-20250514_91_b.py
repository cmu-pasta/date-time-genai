
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def gregorian_to_indian_national_calendar(gregorian_date: datetime) -> int:
    year = gregorian_date.year
    
    # Determine if the Gregorian year is a leap year
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    # Saka new year starts on March 21 in leap years, March 22 in normal years
    saka_new_year_day = 21 if is_leap else 22
    saka_new_year = datetime(year, 3, saka_new_year_day)
    
    # Check if the given date is before or after the Saka new year
    if gregorian_date >= saka_new_year:
        # Same Gregorian year
        saka_year = year - 78
        days_since_saka_new_year = (gregorian_date - saka_new_year).days
    else:
        # Previous Gregorian year's Saka calendar
        prev_year = year - 1
        is_prev_leap = (prev_year % 4 == 0 and prev_year % 100 != 0) or (prev_year % 400 == 0)
        prev_saka_new_year_day = 21 if is_prev_leap else 22
        prev_saka_new_year = datetime(prev_year, 3, prev_saka_new_year_day)
        saka_year = prev_year - 78
        days_since_saka_new_year = (gregorian_date - prev_saka_new_year).days
    
    # Convert days to Saka month and day
    # Month lengths: Chaitra (30/31), then 31,31,31,31,31,30,30,30,30,30,30
    month_lengths = [31 if is_leap else 30, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30]
    
    month = 1
    day = days_since_saka_new_year + 1
    
    for month_length in month_lengths:
        if day <= month_length:
            break
        day -= month_length
        month += 1
    
    # Return in YYYYMMDD format
    return saka_year * 10000 + month * 100 + day

# Entry point: gregorian_to_indian_national_calendar(gregorian_date: datetime) -> int

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_91_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_gregorian_to_indian_national_calendar(gregorian_date):
    result = gregorian_to_indian_national_calendar(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")

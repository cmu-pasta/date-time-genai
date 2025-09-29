
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def gregorian_to_saka_date(gregorian_date: date) -> int:
    # Step 1: Determine if it's a leap year in Gregorian calendar
    is_leap_year = gregorian_date.year % 4 == 0 and (gregorian_date.year % 100 != 0 or gregorian_date.year % 400 == 0)
    
    # Step 2: Determine the start date of Saka year for this Gregorian year
    if is_leap_year:
        saka_start = date(gregorian_date.year, 3, 21)  # March 21 in leap years
    else:
        saka_start = date(gregorian_date.year, 3, 22)  # March 22 in normal years
    
    # Step 3: Calculate Saka year
    if gregorian_date < saka_start:
        saka_year = gregorian_date.year - 79  # Previous Saka year
        # Calculate from previous year's start
        if (gregorian_date.year - 1) % 4 == 0 and ((gregorian_date.year - 1) % 100 != 0 or (gregorian_date.year - 1) % 400 == 0):
            prev_saka_start = date(gregorian_date.year - 1, 3, 21)
        else:
            prev_saka_start = date(gregorian_date.year - 1, 3, 22)
        days_from_start = (gregorian_date - prev_saka_start).days
    else:
        saka_year = gregorian_date.year - 78  # Current Saka year
        days_from_start = (gregorian_date - saka_start).days
    
    # Step 4: Calculate Saka month and day based on days from start
    # Saka calendar months and their days: Chaitra(30/31), then 5 months of 31 days, then 6 months of 30 days
    saka_month_days = [31 if is_leap_year else 30, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30]
    
    saka_month = 1
    saka_day = days_from_start + 1
    
    for month_days in saka_month_days:
        if saka_day <= month_days:
            break
        saka_day -= month_days
        saka_month += 1
    
    # Step 5: Return as integer in YYYYMMDD format
    return saka_year * 10000 + saka_month * 100 + saka_day

# Entry point: gregorian_to_saka_date(gregorian_date: date) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_91_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_saka_date(gregorian_date):
    result = gregorian_to_saka_date(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")

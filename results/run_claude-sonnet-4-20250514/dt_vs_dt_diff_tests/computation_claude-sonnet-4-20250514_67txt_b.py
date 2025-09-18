
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def gregorian_to_hebrew(gregorian_date: date) -> int:
    """
    Convert a Gregorian date to Hebrew calendar date.
    Returns the Hebrew date as an integer in YYYYMMDD format.
    """
    
    # Hebrew calendar epoch: September 7, 3761 BCE (Gregorian)
    # But we'll use January 1, 1 CE as reference point for easier calculation
    # The Hebrew year 1 corresponds to 3760 BCE
    
    # Calculate days since January 1, 1 CE
    epoch = date(1, 1, 1)
    days_since_epoch = (gregorian_date - epoch).days
    
    # Add offset to get to Hebrew calendar epoch (approximately)
    # Hebrew calendar started around 3761 BCE, so we add those days
    hebrew_epoch_offset = 1373429  # Approximate days from 3761 BCE to 1 CE
    hebrew_days = days_since_epoch + hebrew_epoch_offset
    
    # Hebrew calendar average year length (accounting for leap years)
    # Hebrew year is approximately 365.2468 days
    hebrew_year_length = 365.2468
    
    # Calculate approximate Hebrew year
    hebrew_year = int(hebrew_days / hebrew_year_length) + 1
    
    # Adjust for the fact that Hebrew year starts in fall
    # Get remaining days in the current Hebrew year
    days_in_year = hebrew_days - ((hebrew_year - 1) * hebrew_year_length)
    
    # Hebrew months (approximation)
    # Hebrew calendar has 12-13 months depending on leap year
    is_leap_year = (hebrew_year % 19) in [3, 6, 8, 11, 14, 17, 0]
    
    if is_leap_year:
        month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 29]  # 13 months
    else:
        month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]  # 12 months
    
    # Find the Hebrew month and day
    hebrew_month = 1
    remaining_days = int(days_in_year)
    
    for month_length in month_days:
        if remaining_days <= month_length:
            break
        remaining_days -= month_length
        hebrew_month += 1
    
    hebrew_day = max(1, remaining_days)
    
    # Ensure valid ranges
    hebrew_month = min(max(1, hebrew_month), 13)
    hebrew_day = min(max(1, hebrew_day), 30)
    
    # Return as integer in YYYYMMDD format
    return hebrew_year * 10000 + hebrew_month * 100 + hebrew_day

# Entry point: gregorian_to_hebrew(gregorian_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_67txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_hebrew(gregorian_date):
    result = gregorian_to_hebrew(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")

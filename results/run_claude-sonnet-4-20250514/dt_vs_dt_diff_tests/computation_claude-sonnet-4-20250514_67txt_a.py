
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def gregorian_to_hebrew_date(gregorian_date: datetime) -> tuple:
    # Hebrew calendar epoch: October 7, 3761 BCE (Gregorian)
    # This corresponds to 1 Tishrei 1 in Hebrew calendar
    hebrew_epoch = date(1, 10, 7)  # October 7, year 1 CE (adjusted for calculation)
    
    # Convert input datetime to date if needed
    if isinstance(gregorian_date, datetime):
        greg_date = gregorian_date.date()
    else:
        greg_date = gregorian_date
    
    # Calculate days since Hebrew epoch (adjusted for BCE calculation)
    # Hebrew year 1 corresponds to 3761 BCE, so we add 3760 years
    adjusted_epoch = date(greg_date.year - 3760, 10, 7) if greg_date.year >= 3761 else date(1, 10, 7)
    
    # Basic Hebrew calendar calculation
    # Average Hebrew year is approximately 365.2468 days
    days_per_hebrew_year = 365.2468
    
    # Calculate approximate Hebrew year
    days_since_epoch = (greg_date - date(1, 10, 7)).days + (greg_date.year - 1) * 365.25 + 3760 * 365.25
    hebrew_year = int(days_since_epoch / days_per_hebrew_year) + 1
    
    # Simplified month calculation (Hebrew calendar has 12 or 13 months)
    # Average month length is about 29.53 days
    days_per_month = 29.53
    
    # Calculate days into the Hebrew year
    year_start_days = (hebrew_year - 1) * days_per_hebrew_year
    days_into_year = days_since_epoch - year_start_days
    
    # Calculate Hebrew month (1-13)
    hebrew_month = min(int(days_into_year / days_per_month) + 1, 13)
    
    # Calculate Hebrew day
    month_start_days = (hebrew_month - 1) * days_per_month
    hebrew_day = int(days_into_year - month_start_days) + 1
    
    # Ensure day is at least 1
    hebrew_day = max(1, hebrew_day)
    
    return int(hebrew_year), int(hebrew_month), int(hebrew_day)

def get_hebrew_year(gregorian_date: datetime) -> int:
    year, month, day = gregorian_to_hebrew_date(gregorian_date)
    return year

def get_hebrew_month(gregorian_date: datetime) -> int:
    year, month, day = gregorian_to_hebrew_date(gregorian_date)
    return month

def get_hebrew_day(gregorian_date: datetime) -> int:
    year, month, day = gregorian_to_hebrew_date(gregorian_date)
    return day

# Entry point: get_hebrew_year(gregorian_date: datetime) -> int
# Entry point: get_hebrew_month(gregorian_date: datetime) -> int  
# Entry point: get_hebrew_day(gregorian_date: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_67txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_hebrew_year(gregorian_date):
    result = get_hebrew_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")

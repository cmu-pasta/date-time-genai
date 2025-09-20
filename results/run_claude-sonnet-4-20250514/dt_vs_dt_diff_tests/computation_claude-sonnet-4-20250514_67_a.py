
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def gregorian_to_hebrew(dt: datetime) -> int:
    # Hebrew calendar epoch: September 7, 3761 BCE (Gregorian)
    # This represents 1 Tishrei 1 in Hebrew calendar
    
    # Get the Gregorian date components
    year = dt.year
    month = dt.month
    day = dt.day
    
    # Convert to Julian day number first
    if month <= 2:
        year -= 1
        month += 12
    
    a = year // 100
    b = 2 - a + a // 4
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524
    
    # Hebrew calendar calculations
    # Hebrew epoch in Julian days: 347998 (corresponds to 1 Tishrei 1)
    hebrew_epoch = 347998
    
    days_since_epoch = jd - hebrew_epoch
    
    # Approximate Hebrew year (Hebrew years are approximately 365.25 days)
    hebrew_year = int(days_since_epoch / 365.25) + 1
    
    # Refine the Hebrew year calculation
    # This is a simplified approximation
    days_in_hebrew_year = 354  # Basic lunar year
    if hebrew_year % 19 in [3, 6, 8, 11, 14, 17, 0]:  # Leap years in 19-year cycle
        days_in_hebrew_year = 384
    
    # Adjust for more accurate year
    while days_since_epoch >= days_in_hebrew_year * hebrew_year:
        hebrew_year += 1
    
    # Calculate remaining days in the year
    year_start_days = days_in_hebrew_year * (hebrew_year - 1)
    days_in_current_year = days_since_epoch - year_start_days
    
    # Hebrew months (simplified - using average month lengths)
    month_lengths = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]  # 12 months
    if hebrew_year % 19 in [3, 6, 8, 11, 14, 17, 0]:  # Leap year
        month_lengths.insert(6, 29)  # Add Adar I
    
    hebrew_month = 1
    hebrew_day = days_in_current_year + 1
    
    # Find the correct month
    for i, length in enumerate(month_lengths):
        if hebrew_day <= length:
            hebrew_month = i + 1
            break
        hebrew_day -= length
    
    # Ensure day is at least 1
    if hebrew_day < 1:
        hebrew_day = 1
    
    # Format as integer: YYYYMMDD
    return hebrew_year * 10000 + hebrew_month * 100 + hebrew_day

# Entry point: gregorian_to_hebrew(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_67_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_gregorian_to_hebrew(dt):
    result = gregorian_to_hebrew(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

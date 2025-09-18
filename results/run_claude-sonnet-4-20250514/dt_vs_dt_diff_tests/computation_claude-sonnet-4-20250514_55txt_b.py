
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def gregorian_to_islamic_date(gregorian_date: date) -> int:
    # Islamic calendar epoch: July 16, 622 CE
    islamic_epoch = date(622, 7, 16)
    
    # Calculate days since Islamic epoch
    if gregorian_date < islamic_epoch:
        return 0  # Invalid date before Islamic calendar started
    
    days_since_epoch = (gregorian_date - islamic_epoch).days
    
    # Average Islamic year length (354.37 days)
    # Average Islamic month length (29.53 days)
    islamic_year_length = 354.37
    islamic_month_length = 29.53
    
    # Calculate Islamic year (starting from year 1)
    islamic_year = int(days_since_epoch / islamic_year_length) + 1
    
    # Calculate remaining days after full years
    remaining_days = days_since_epoch - ((islamic_year - 1) * islamic_year_length)
    
    # Calculate Islamic month (1-12)
    islamic_month = int(remaining_days / islamic_month_length) + 1
    if islamic_month > 12:
        islamic_month = 12
    
    # Calculate Islamic day (1-30)
    islamic_day = int(remaining_days - ((islamic_month - 1) * islamic_month_length)) + 1
    if islamic_day < 1:
        islamic_day = 1
    elif islamic_day > 30:
        islamic_day = 30
    
    # Return as a combined integer: YYYYMMDD format
    return int(f"{islamic_year:04d}{islamic_month:02d}{islamic_day:02d}")

# Entry point: gregorian_to_islamic_date(gregorian_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_55txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_islamic_date(gregorian_date):
    result = gregorian_to_islamic_date(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def gregorian_to_islamic(gregorian_date: datetime) -> int:
    # Islamic epoch: July 16, 622 CE (approximately)
    islamic_epoch = datetime(622, 7, 16)
    
    # If the date is before the Islamic epoch, return 0 (invalid)
    if gregorian_date < islamic_epoch:
        return 0
    
    # Calculate days since Islamic epoch
    delta = gregorian_date - islamic_epoch
    days_since_epoch = delta.days
    
    # Average lengths in days
    islamic_year_avg = 354.37
    islamic_month_avg = 29.53
    
    # Calculate Islamic year (approximate)
    islamic_year = int(days_since_epoch / islamic_year_avg) + 1
    
    # Calculate remaining days after accounting for complete years
    remaining_days = days_since_epoch - int((islamic_year - 1) * islamic_year_avg)
    
    # Calculate Islamic month (approximate)
    islamic_month = int(remaining_days / islamic_month_avg) + 1
    if islamic_month > 12:
        islamic_month = 12
    elif islamic_month < 1:
        islamic_month = 1
    
    # Calculate Islamic day (approximate)
    days_in_previous_months = int((islamic_month - 1) * islamic_month_avg)
    islamic_day = remaining_days - days_in_previous_months + 1
    if islamic_day > 30:
        islamic_day = 30
    elif islamic_day < 1:
        islamic_day = 1
    
    # Return as integer in YYYYMMDD format
    return int(islamic_year * 10000 + islamic_month * 100 + int(islamic_day))

# Entry point: gregorian_to_islamic(gregorian_date: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_55_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_gregorian_to_islamic(gregorian_date):
    result = gregorian_to_islamic(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")

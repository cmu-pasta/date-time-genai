
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def gregorian_to_islamic_year(gregorian_date: date) -> int:
    # Islamic calendar epoch: July 16, 622 CE (Gregorian)
    islamic_epoch = date(622, 7, 16)
    
    # Calculate days since Islamic epoch
    days_since_epoch = (gregorian_date - islamic_epoch).days
    
    # Average length of an Islamic year in days (354.367 days)
    # Islamic calendar is lunar-based with 12 months averaging 29.53 days each
    avg_islamic_year_days = 354.367
    
    # Calculate Islamic year
    # Adding 1 because the Islamic calendar starts from year 1 AH
    islamic_year = int(days_since_epoch / avg_islamic_year_days) + 1
    
    # Ensure we don't return negative years for dates before the epoch
    if islamic_year < 1:
        islamic_year = 1
    
    return islamic_year

# Entry point: gregorian_to_islamic_year(gregorian_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_55txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_islamic_year(gregorian_date):
    result = gregorian_to_islamic_year(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def gregorian_to_islamic(gregorian_date: date) -> date:
    # Islamic epoch: July 16, 622 CE (Gregorian)
    islamic_epoch = date(622, 7, 16)
    
    # Calculate days since Islamic epoch
    if gregorian_date < islamic_epoch:
        # Handle dates before Islamic epoch
        days_diff = (islamic_epoch - gregorian_date).days
        # For simplicity, return epoch date for pre-Islamic dates
        return date(1, 1, 1)
    else:
        days_since_epoch = (gregorian_date - islamic_epoch).days
    
    # Average Islamic year is approximately 354.367 days
    # Average Islamic month is approximately 29.531 days
    avg_year_days = 354.367
    avg_month_days = 29.531
    
    # Calculate approximate Islamic year
    islamic_year = int(days_since_epoch / avg_year_days) + 1
    
    # Calculate remaining days after full years
    remaining_days = days_since_epoch - int((islamic_year - 1) * avg_year_days)
    
    # Calculate Islamic month
    islamic_month = min(12, max(1, int(remaining_days / avg_month_days) + 1))
    
    # Calculate remaining days for the day of month
    days_in_prev_months = (islamic_month - 1) * avg_month_days
    islamic_day = max(1, min(30, int(remaining_days - days_in_prev_months) + 1))
    
    # Ensure valid day for the month (Islamic months have 29 or 30 days)
    if islamic_month in [1, 3, 5, 7, 9, 11]:  # Odd months typically have 30 days
        max_days = 30
    else:  # Even months typically have 29 days
        max_days = 29
    
    islamic_day = min(islamic_day, max_days)
    
    # Create and return the Islamic date as a standard date object
    # Note: This is an approximation and may not be completely accurate
    return date(islamic_year, islamic_month, islamic_day)

# Entry point: gregorian_to_islamic(gregorian_date: date) -> date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_55_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_gregorian_to_islamic(gregorian_date):
    result = gregorian_to_islamic(gregorian_date)
    formatted_result = format_value_dt(result, gregorian_date)
    log_file.write(formatted_result + "\n")

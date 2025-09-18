
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def get_japanese_calendar_year(input_date: datetime) -> int:
    # Convert datetime to date for easier comparison
    if isinstance(input_date, datetime):
        target_date = input_date.date()
    else:
        target_date = input_date
    
    # Define era start dates
    reiwa_start = date(2019, 5, 1)  # Reiwa era started May 1, 2019
    heisei_start = date(1989, 1, 8)  # Heisei era started January 8, 1989
    showa_start = date(1926, 12, 25) # Showa era started December 25, 1926
    taisho_start = date(1912, 7, 30) # Taisho era started July 30, 1912
    meiji_start = date(1868, 1, 25)  # Meiji era started January 25, 1868
    
    # Determine era and calculate Japanese year
    if target_date >= reiwa_start:
        # Reiwa era
        japanese_year = (target_date.year - reiwa_start.year) + 1
        if target_date.month < reiwa_start.month or (target_date.month == reiwa_start.month and target_date.day < reiwa_start.day):
            japanese_year -= 1
        return max(1, japanese_year)
    
    elif target_date >= heisei_start:
        # Heisei era
        japanese_year = (target_date.year - heisei_start.year) + 1
        if target_date.month < heisei_start.month or (target_date.month == heisei_start.month and target_date.day < heisei_start.day):
            japanese_year -= 1
        return max(1, japanese_year)
    
    elif target_date >= showa_start:
        # Showa era
        japanese_year = (target_date.year - showa_start.year) + 1
        if target_date.month < showa_start.month or (target_date.month == showa_start.month and target_date.day < showa_start.day):
            japanese_year -= 1
        return max(1, japanese_year)
    
    elif target_date >= taisho_start:
        # Taisho era
        japanese_year = (target_date.year - taisho_start.year) + 1
        if target_date.month < taisho_start.month or (target_date.month == taisho_start.month and target_date.day < taisho_start.day):
            japanese_year -= 1
        return max(1, japanese_year)
    
    elif target_date >= meiji_start:
        # Meiji era
        japanese_year = (target_date.year - meiji_start.year) + 1
        if target_date.month < meiji_start.month or (target_date.month == meiji_start.month and target_date.day < meiji_start.day):
            japanese_year -= 1
        return max(1, japanese_year)
    
    else:
        # Before Meiji era - return 0 to indicate pre-modern era
        return 0

# Entry point: get_japanese_calendar_year(input_date: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_85txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_japanese_calendar_year(input_date):
    result = get_japanese_calendar_year(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")

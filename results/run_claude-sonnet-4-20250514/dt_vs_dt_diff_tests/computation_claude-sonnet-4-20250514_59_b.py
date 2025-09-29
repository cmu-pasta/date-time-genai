
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_chinese_new_year(year: int) -> datetime:
    # Dictionary mapping years to Chinese New Year dates (month, day)
    chinese_new_year_dates = {
        2020: (1, 25), 2021: (2, 12), 2022: (2, 1), 2023: (1, 22), 2024: (2, 10),
        2025: (1, 29), 2026: (2, 17), 2027: (2, 6), 2028: (1, 26), 2029: (2, 13),
        2030: (2, 3), 2031: (1, 23), 2032: (2, 11), 2033: (1, 31), 2034: (2, 19),
        2035: (2, 8), 2036: (1, 28), 2037: (2, 15), 2038: (2, 4), 2039: (1, 24),
        2040: (2, 12), 2041: (2, 1), 2042: (1, 22), 2043: (2, 10), 2044: (1, 30),
        2045: (2, 17), 2046: (2, 6), 2047: (1, 26), 2048: (2, 14), 2049: (2, 2),
        2050: (1, 23)
    }
    
    # Check if the year is in our lookup table
    if year in chinese_new_year_dates:
        month, day = chinese_new_year_dates[year]
        return datetime(year, month, day)
    else:
        # For years outside our range, use an approximation
        # Chinese New Year typically occurs between Jan 21 and Feb 20
        # Use a simple approximation based on the lunar cycle (approximately 29.5 days)
        base_year = 2024
        base_date = datetime(2024, 2, 10)  # Chinese New Year 2024
        
        years_diff = year - base_year
        # Approximate lunar year is about 354 days, Gregorian year is 365.25 days
        # The difference accumulates over time
        days_offset = years_diff * 11  # Approximate drift per year
        
        approximate_date = base_date.replace(year=year)
        
        # Adjust for the approximate offset
        if days_offset > 0:
            # Move backwards for future years
            approximate_date = approximate_date.replace(day=max(1, approximate_date.day - (days_offset % 30)))
        else:
            # Move forwards for past years
            approximate_date = approximate_date.replace(day=min(28, approximate_date.day + (abs(days_offset) % 30)))
        
        return approximate_date

# Entry point: find_chinese_new_year(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_59_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_chinese_new_year(year):
    result = find_chinese_new_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

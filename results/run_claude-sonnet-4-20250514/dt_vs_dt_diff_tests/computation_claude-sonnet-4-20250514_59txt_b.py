
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import math
def find_chinese_new_year(year: int) -> datetime:
    # Winter solstice is approximately December 21
    winter_solstice = datetime(year - 1, 12, 21)
    
    # Average lunar month length in days
    lunar_month = 29.53059
    
    # Chinese New Year is approximately the second new moon after winter solstice
    # We use a base reference: January 1, 1900 was close to a new moon
    # This is a simplified approximation
    base_date = datetime(1900, 1, 1)
    days_since_base = (winter_solstice - base_date).days
    
    # Calculate lunar cycles since base date
    lunar_cycles = days_since_base / lunar_month
    
    # Find the next new moon after winter solstice (approximately)
    cycles_to_next_new_moon = math.ceil(lunar_cycles) - lunar_cycles
    days_to_next_new_moon = cycles_to_next_new_moon * lunar_month
    
    # First new moon after winter solstice
    first_new_moon = winter_solstice + timedelta(days=days_to_next_new_moon)
    
    # Second new moon (Chinese New Year approximation)
    chinese_new_year = first_new_moon + timedelta(days=lunar_month)
    
    # Adjust to the actual year if the calculation went into the next year
    if chinese_new_year.year != year:
        # Recalculate for the current year's winter solstice
        winter_solstice = datetime(year, 12, 21)
        days_since_base = (winter_solstice - base_date).days
        lunar_cycles = days_since_base / lunar_month
        cycles_to_next_new_moon = math.ceil(lunar_cycles) - lunar_cycles
        days_to_next_new_moon = cycles_to_next_new_moon * lunar_month
        first_new_moon = winter_solstice + timedelta(days=days_to_next_new_moon)
        chinese_new_year = first_new_moon + timedelta(days=lunar_month)
        
        # If still not in the target year, use previous year's calculation
        if chinese_new_year.year != year:
            winter_solstice = datetime(year - 1, 12, 21)
            days_since_base = (winter_solstice - base_date).days
            lunar_cycles = days_since_base / lunar_month
            cycles_to_next_new_moon = math.ceil(lunar_cycles) - lunar_cycles
            days_to_next_new_moon = cycles_to_next_new_moon * lunar_month
            first_new_moon = winter_solstice + timedelta(days=days_to_next_new_moon)
            chinese_new_year = first_new_moon + timedelta(days=lunar_month)
    
    return datetime(chinese_new_year.year, chinese_new_year.month, chinese_new_year.day)

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_59txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_chinese_new_year(year):
    result = find_chinese_new_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

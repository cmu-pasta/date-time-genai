
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_date_to_roman_year(dt: datetime) -> str:
    # Step 1: Extract the year from the datetime object
    year = dt.year
    
    # Step 2: Convert the year to Roman numerals
    # Define the mapping of values to Roman numerals in descending order
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    roman_chars = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    
    # Build the Roman numeral representation
    roman_year = ''
    for i in range(len(values)):
        count = year // values[i]
        if count:
            roman_year += roman_chars[i] * count
            year -= values[i] * count
    
    return roman_year

# Entry point: convert_date_to_roman_year(dt: datetime) -> str

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_52_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_date_to_roman_year(dt):
    result = convert_date_to_roman_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

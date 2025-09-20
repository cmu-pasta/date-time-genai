
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_year_to_roman_numeral(dt: datetime) -> str:
    # Step 1: Extract the year from the datetime object
    year = dt.year

    # Step 2: Define the Roman numeral mapping
    # This list is ordered from largest to smallest for efficient conversion
    roman_map = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    # Step 3: Convert the year to its Roman numeral representation
    roman_numeral = []
    for value, symbol in roman_map:
        while year >= value:
            roman_numeral.append(symbol)
            year -= value
            
    # Step 4: Join the list of symbols to form the final Roman numeral string
    return "".join(roman_numeral)

# Entry point: convert_year_to_roman_numeral(dt: datetime) -> str

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_52_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_year_to_roman_numeral(dt):
    result = convert_year_to_roman_numeral(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

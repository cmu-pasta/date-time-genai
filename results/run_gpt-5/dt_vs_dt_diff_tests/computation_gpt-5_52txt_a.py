
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def _int_to_roman_year(year: int) -> str:
    # Ensure the year is within the valid Gregorian proleptic range used by datetime (1..9999)
    if year < 1 or year > 9999:
        raise ValueError("Year must be between 1 and 9999 inclusive.")
    
    # Roman numeral mapping
    numerals = [
        (1000, "M"), (900, "CM"),
        (500, "D"),  (400, "CD"),
        (100, "C"),  (90, "XC"),
        (50, "L"),   (40, "XL"),
        (10, "X"),   (9, "IX"),
        (5, "V"),    (4, "IV"),
        (1, "I"),
    ]
    
    # For years > 3999, extend by repeating 'M' (common ASCII-friendly approach)
    n = year
    result = []
    for value, symbol in numerals:
        if n == 0:
            break
        count, n = divmod(n, value)
        if count:
            result.append(symbol * count)
    return "".join(result)

def date_to_roman_year(d: date) -> str:
    """
    Convert the year component of a date or datetime to its Roman numeral representation.
    Accepts: datetime.date or datetime.datetime (both have a 'year' attribute)
    Returns: str containing the Roman numeral year
    """
    # Supports both date and datetime since both provide 'year'
    yr = d.year
    return _int_to_roman_year(yr)

# Entry point: date_to_roman_year(d: date) -> str

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_52txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_to_roman_year(d):
    result = date_to_roman_year(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")

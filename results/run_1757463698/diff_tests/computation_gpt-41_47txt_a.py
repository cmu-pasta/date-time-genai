
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def count_public_holidays_between(start_date: date, end_date: date, country_code: str) -> int:
    """
    Counts the number of public holidays between two dates for a given country code.
    Dates are inclusive.
    For demonstration, this function only supports 'US' with a static set of holidays.
    """
    # Step 1: Define a minimal public holiday calendar for demonstration
    # For 'US', consider a few example holidays; adjust the years as needed
    def us_holidays(year: int):
        return [
            date(year, 1, 1),   # New Year's Day
            date(year, 7, 4),   # Independence Day
            date(year, 12, 25), # Christmas Day
        ]
    # Add more country codes and their holidays here as needed
    
    # Step 2: Normalize input order and determine the relevant years
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    years = range(start_date.year, end_date.year + 1)    
    
    # Step 3: Collect public holidays within the range based on country_code
    holiday_count = 0
    for year in years:
        if country_code == "US":
            for holiday in us_holidays(year):
                if start_date <= holiday <= end_date:
                    holiday_count += 1
        # Add other country codes here as needed

    # Step 4: Return the computed count
    return holiday_count

# Entry point: count_public_holidays_between(start_date: date, end_date: date, country_code: str) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_47txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy(), string_strategy())
def test_count_public_holidays_between(start_date, end_date, country_code):
    result = count_public_holidays_between(start_date, end_date, country_code)
    formatted_result = format_value_dt(result, start_date, end_date, country_code)
    log_file.write(formatted_result + "\n")

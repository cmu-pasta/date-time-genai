
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_public_holidays_between(start_date: date, end_date: date, country_code: str) -> int:
    # Step 1: Ensure correct ordering of dates
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    # Step 2: For the supported country (US), define a set of fixed-date public holidays
    # (for demonstration, we'll use major US federal holidays)
    def get_us_public_holidays(year: int):
        holidays = [
            date(year, 1, 1),   # New Year's Day
            date(year, 7, 4),   # Independence Day
            date(year, 12, 25), # Christmas Day
        ]
        return holidays

    # Step 3: For each year in the range, collect applicable holidays
    years = range(start_date.year, end_date.year + 1)
    public_holiday_count = 0

    if country_code.upper() == 'US':
        for yr in years:
            for holiday in get_us_public_holidays(yr):
                if start_date <= holiday <= end_date:
                    public_holiday_count += 1
    else:
        # Step 4: If country code not supported, count as 0
        public_holiday_count = 0

    # Step 5: Return the result as an integer
    return public_holiday_count

# Entry point: calculate_public_holidays_between(start_date: date, end_date: date, country_code: str) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_47txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy(), string_strategy())
def test_calculate_public_holidays_between(start_date, end_date, country_code):
    result = calculate_public_holidays_between(start_date, end_date, country_code)
    formatted_result = format_value_dt(result, start_date, end_date, country_code)
    log_file.write(formatted_result + "\n")


import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def is_us_federal_holiday(check_date: date) -> bool:
    # Helper to find the nth weekday in a month
    def nth_weekday(year, month, weekday, n):
        d = date(year, month, 1)
        days_to_add = (weekday - d.weekday() + 7) % 7
        result = d + timedelta(days=days_to_add + 7*(n-1))
        return result

    # Helper to find the last weekday in a month
    def last_weekday(year, month, weekday):
        d = date(year, month+1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
        days_to_subtract = (d.weekday() - weekday + 7) % 7
        return d - timedelta(days=days_to_subtract)

    year = check_date.year
    
    # Fixed date holidays
    new_years = date(year, 1, 1)
    independence = date(year, 7, 4)
    veterans = date(year, 11, 11)
    christmas = date(year, 12, 25)
    
    # Variable holidays
    martin_luther_king = nth_weekday(year, 1, 0, 3)          # 3rd Monday in Jan
    washington_birthday = nth_weekday(year, 2, 0, 3)         # 3rd Monday in Feb
    memorial = last_weekday(year, 5, 0)                      # Last Monday in May
    labor = nth_weekday(year, 9, 0, 1)                       # 1st Monday in Sep
    columbus = nth_weekday(year, 10, 0, 2)                   # 2nd Monday in Oct
    thanksgiving = nth_weekday(year, 11, 3, 4)               # 4th Thursday in Nov
    
    # Observed holidays (if fixed-date holiday falls on weekend)
    holidays = set()
    for holiday in [new_years, independence, veterans, christmas]:
        holidays.add(holiday)
        if holiday.weekday() == 5:      # Saturday
            holidays.add(holiday - timedelta(days=1))
        elif holiday.weekday() == 6:    # Sunday
            holidays.add(holiday + timedelta(days=1))
            
    # Add variable-date holidays
    holidays.update([
        martin_luther_king,
        washington_birthday,
        memorial,
        labor,
        columbus,
        thanksgiving
    ])
    
    return check_date in holidays

# Entry point: is_us_federal_holiday(check_date: date) -> bool

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_33txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_is_us_federal_holiday(check_date):
    result = is_us_federal_holiday(check_date)
    formatted_result = format_value_dt(result, check_date)
    log_file.write(formatted_result + "\n")

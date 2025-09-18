
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def find_autumnal_equinox(year: int) -> date:
    # Approximation formula for autumnal equinox
    # This formula gives the day of year (1-365/366) for the autumnal equinox
    
    # Base calculation using astronomical approximation
    # The formula accounts for the gradual shift in equinox timing
    day_of_year = 266 + (year - 2000) * 0.24219 - int((year - 2000) / 4)
    
    # Ensure the result is within valid range
    day_of_year = int(round(day_of_year))
    
    # Handle leap years and boundary conditions
    if day_of_year < 1:
        day_of_year = 1
    elif day_of_year > 366:
        day_of_year = 366
    
    # Convert day of year to actual date
    # Start with January 1st of the given year
    jan_first = datetime(year, 1, 1)
    
    # Add the calculated number of days (subtract 1 since day 1 is Jan 1st)
    equinox_date = jan_first + timedelta(days=day_of_year - 1)
    
    return equinox_date.date()

# Entry point: find_autumnal_equinox(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_53txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_autumnal_equinox(year):
    result = find_autumnal_equinox(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

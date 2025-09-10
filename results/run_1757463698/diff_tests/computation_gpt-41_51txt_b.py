
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta, datetime
def get_first_full_moon(year: int) -> date:
    """
    Returns the date of the first full moon in the given year.
    Uses an average synodic month approximation.
    """
    # Step 1: Define base known full moon: January 21, 2000, 00:40 UTC
    base_full_moon = datetime(2000, 1, 21, 0, 40)
    # Average synodic month (full moon to full moon), in days
    synodic_month = 29.530588853

    # Step 2: Start from the base date and increment by synodic months until reaching the target year
    approx_full_moon = base_full_moon
    while approx_full_moon.year < year:
        approx_full_moon += timedelta(days=synodic_month)
    
    # Step 3: If we've passed the year, we need the first in the year
    while approx_full_moon.year == year - 1:
        approx_full_moon += timedelta(days=synodic_month)
    # Step 4: Return just the date part
    if approx_full_moon.year == year:
        return approx_full_moon.date()
    else:
        # This can rarely happen due to the drift, so go back one
        prev_full_moon = approx_full_moon - timedelta(days=synodic_month)
        if prev_full_moon.year == year:
            return prev_full_moon.date()
        else:
            raise Exception("Could not compute first full moon for the given year.")

# Entry point: get_first_full_moon(year: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_51txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_get_first_full_moon(year):
    result = get_first_full_moon(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")

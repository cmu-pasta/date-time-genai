
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def count_full_moons_between(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Define a reference full moon datetime (Jan 21, 2000 at 00:40 UTC)
    reference_full_moon = datetime(2000, 1, 21, 0, 40)
    synodic_month = 29.530588853  # days between full moons
    
    # Step 2: Sort input datetimes so start <= end
    start = min(dt1, dt2)
    end = max(dt1, dt2)
    
    # Step 3: Calculate days from reference to start and end
    days_from_reference_to_start = (start - reference_full_moon).total_seconds() / 86400
    days_from_reference_to_end = (end - reference_full_moon).total_seconds() / 86400

    # Step 4: Number of full moons passed up to start and end (using floor to count *full* moons)
    moons_at_start = int(days_from_reference_to_start // synodic_month)
    moons_at_end = int(days_from_reference_to_end // synodic_month)
    
    # Step 5: The count of full moons between start and end is the difference
    full_moons_between = abs(moons_at_end - moons_at_start)
    return full_moons_between

# Entry point: count_full_moons_between(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_62txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_count_full_moons_between(dt1, dt2):
    result = count_full_moons_between(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")

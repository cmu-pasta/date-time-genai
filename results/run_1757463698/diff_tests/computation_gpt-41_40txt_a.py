
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def get_moon_phase(dt: date) -> int:
    # Step 1: Select a known new moon date as epoch (January 6, 2000)
    known_new_moon = date(2000, 1, 6)
    
    # Step 2: Calculate the difference in days between the input date and the epoch
    days_difference = (dt - known_new_moon).days
    
    # Step 3: Define the length of the synodic month (full lunar cycle) in days
    synodic_month = 29.53058867
    
    # Step 4: Calculate moon's age in the current cycle
    moon_age = days_difference % synodic_month
    
    # Step 5: Assign phase based on moon age
    # Phase bins: 0 = New Moon, 1 = First Quarter, 2 = Full Moon, 3 = Last Quarter
    # We'll use approximate cutoffs
    if moon_age < 1.84566:
        phase = 0  # New Moon
    elif moon_age < 7.382646:
        phase = 1  # First Quarter (Waxing Crescent)
    elif moon_age < 14.765293:
        phase = 2  # Full Moon (Waxing/Full)
    elif moon_age < 22.147939:
        phase = 3  # Last Quarter (Waning Gibbous)
    else:
        phase = 0  # New Moon (Waning Crescent to New)

    return phase

# Entry point: get_moon_phase(dt: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_40txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_get_moon_phase(dt):
    result = get_moon_phase(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

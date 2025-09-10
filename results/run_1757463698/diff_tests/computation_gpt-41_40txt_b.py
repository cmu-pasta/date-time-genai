
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def determine_moon_phase(dt: date) -> int:
    """
    Determines the moon phase for a given date.
    
    Returns:
        An integer in 0-7, where:
        0 - New Moon
        1 - Waxing Crescent
        2 - First Quarter
        3 - Waxing Gibbous
        4 - Full Moon
        5 - Waning Gibbous
        6 - Last Quarter
        7 - Waning Crescent
    """
    # Reference new moon: January 6, 2000 (known new moon date)
    known_new_moon = date(2000, 1, 6)
    synodic_month = 29.530588853  # Average length of a lunar month, in days

    # Step 1: Calculate number of days since known new moon
    days_since_known_new = (dt - known_new_moon).days

    # Step 2: Find the position in the lunar month
    new_moons = days_since_known_new / synodic_month
    position = new_moons - int(new_moons)
    if position < 0:
        position += 1.0  # Ensure it's always positive

    # Step 3: Map position [0.0, 1.0) to phase index 0-7
    phase_index = int((position * 8) + 0.5) % 8

    # Step 4: Return the moon phase as integer
    return phase_index

# Entry point: determine_moon_phase(dt: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_40txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_determine_moon_phase(dt):
    result = determine_moon_phase(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

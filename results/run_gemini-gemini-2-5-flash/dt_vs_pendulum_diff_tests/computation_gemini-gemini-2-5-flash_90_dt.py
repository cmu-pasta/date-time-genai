
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def calculate_lunar_age(current_dt: datetime) -> int:
    # Step 1: Define a known New Moon reference date (January 6, 2000, 00:00:00 UTC was a New Moon)
    # Using a datetime object for consistency, though only date part is strictly needed for rough days
    EPOCH_NEW_MOON = datetime(2000, 1, 6)
    
    # Step 2: Define the average length of a synodic month in days
    SYNODIC_MONTH_LENGTH = 29.530588

    # Step 3: Calculate the total number of days between the current date and the epoch new moon
    # Convert datetimes to dates to get whole day difference consistently, though timedelta handles it
    total_days_since_epoch = (current_dt.date() - EPOCH_NEW_MOON.date()).days
    
    # Step 4: Calculate the lunar age using the modulo operator
    # The result represents days into the current lunar cycle
    lunar_age_float = total_days_since_epoch % SYNODIC_MONTH_LENGTH
    
    # Ensure the result is non-negative if total_days_since_epoch was negative
    if lunar_age_float < 0:
        lunar_age_float += SYNODIC_MONTH_LENGTH

    # Step 5: Round the lunar age to the nearest integer as requested (days since new moon implies integer)
    return round(lunar_age_float)

# Entry point: calculate_lunar_age(current_dt: datetime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_90_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_lunar_age(current_dt):
    result = calculate_lunar_age(current_dt)
    formatted_result = format_value_dt(result, current_dt)
    log_file.write(formatted_result + "\n")

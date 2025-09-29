
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_solar_eclipse(reference_date: datetime, latitude: float, longitude: float) -> datetime:
    # Simplified approach using approximate Saros cycle (18 years, 11 days, 8 hours)
    # This is a very rough approximation since actual eclipse calculations require
    # complex astronomical computations not available in the datetime library
    
    # Base reference: A known solar eclipse date (August 21, 2017)
    base_eclipse = datetime(2017, 8, 21, 18, 26)  # Total solar eclipse over USA
    
    # Saros cycle: approximately 6585.3211 days
    saros_days = 6585
    saros_hours = 8  # Additional ~8 hours for more precision
    
    # Calculate how many Saros cycles have passed since the base eclipse
    days_since_base = (reference_date - base_eclipse).days
    
    if days_since_base < 0:
        # If reference date is before base eclipse, return the base eclipse
        return base_eclipse
    
    # Find the next eclipse in the cycle
    cycles_passed = days_since_base // saros_days
    next_eclipse_date = base_eclipse + timedelta(days=(cycles_passed + 1) * saros_days, hours=saros_hours)
    
    # Simple location-based adjustment (very rough approximation)
    # Adjust by up to +/- 1 day based on longitude difference from reference location
    reference_longitude = -97.0  # Approximate longitude of 2017 eclipse path
    longitude_adjustment_hours = int((longitude - reference_longitude) * 0.25)  # Very rough estimation
    
    next_eclipse_date = next_eclipse_date + timedelta(hours=longitude_adjustment_hours)
    
    # Ensure we return a date after the reference date
    if next_eclipse_date <= reference_date:
        next_eclipse_date = next_eclipse_date + timedelta(days=saros_days, hours=saros_hours)
    
    return next_eclipse_date

# Entry point: find_next_solar_eclipse(reference_date: datetime, latitude: float, longitude: float) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_95_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy(), float_strategy())
def test_find_next_solar_eclipse(reference_date, latitude, longitude):
    result = find_next_solar_eclipse(reference_date, latitude, longitude)
    formatted_result = format_value_dt(result, reference_date, latitude, longitude)
    log_file.write(formatted_result + "\n")

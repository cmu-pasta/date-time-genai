
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_next_solar_eclipse(latitude: float, longitude: float, current_date: datetime) -> datetime:
    # Step 1: Define approximate Saros cycle duration (18 years, 11 days, 8 hours)
    saros_cycle_days = 6585.32  # approximately 18 years, 11 days, 8 hours in days
    
    # Step 2: Use a known reference eclipse date (August 21, 2017 - Total Solar Eclipse)
    reference_eclipse = datetime(2017, 8, 21, 18, 26, 40)  # UTC time
    
    # Step 3: Calculate cycles since reference eclipse
    days_since_reference = (current_date - reference_eclipse).total_seconds() / (24 * 3600)
    
    # Step 4: Find the next eclipse in the cycle
    if days_since_reference < 0:
        # If current date is before reference, the reference itself might be the next
        next_eclipse = reference_eclipse
    else:
        # Calculate how many complete cycles have passed
        complete_cycles = int(days_since_reference / saros_cycle_days)
        
        # Calculate the next eclipse date
        next_eclipse = reference_eclipse + timedelta(days=(complete_cycles + 1) * saros_cycle_days)
    
    # Step 5: Apply location-based adjustment (simplified)
    # Adjust based on longitude for approximate local visibility timing
    longitude_adjustment_hours = longitude / 15.0  # Rough timezone adjustment
    location_adjusted_eclipse = next_eclipse + timedelta(hours=longitude_adjustment_hours)
    
    # Step 6: Ensure the eclipse date is after the current date
    while location_adjusted_eclipse <= current_date:
        location_adjusted_eclipse = location_adjusted_eclipse + timedelta(days=saros_cycle_days)
    
    return location_adjusted_eclipse

# Entry point: find_next_solar_eclipse(latitude: float, longitude: float, current_date: datetime) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_95_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), float_strategy(), datetime_strategy())
def test_find_next_solar_eclipse(latitude, longitude, current_date):
    result = find_next_solar_eclipse(latitude, longitude, current_date)
    formatted_result = format_value_dt(result, latitude, longitude, current_date)
    log_file.write(formatted_result + "\n")

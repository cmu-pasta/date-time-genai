
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time, timedelta, datetime
def convert_12hr_to_24hr_time(input_time_12hr: time, is_pm: bool) -> time:
    """
    Converts a time (provided in 12-hour format context) to a 24-hour time object.
    
    Args:
        input_time_12hr: A datetime.time object where the hour component is
                         assumed to be from a 12-hour clock (1-12).
        is_pm: A boolean indicating if the time is PM (True) or AM (False).
               This resolves the 12-hour ambiguity.

    Returns:
        A datetime.time object representing the time in 24-hour format.
    """
    
    # Extract components from the input time
    hour = input_time_12hr.hour
    
    # Apply 12-hour to 24-hour conversion logic
    if is_pm:
        if hour == 12:
            # 12 PM is 12:00 in 24-hour format
            converted_hour = 12
        else:
            # For 1 PM to 11 PM, add 12 to the hour
            converted_hour = hour + 12
    else: # is_am
        if hour == 12:
            # 12 AM is 00:00 in 24-hour format
            converted_hour = 0
        else:
            # For 1 AM to 11 AM, the hour remains the same
            converted_hour = hour
            
    # Create and return the new time object with the converted hour
    return time(
        hour=converted_hour,
        minute=input_time_12hr.minute,
        second=input_time_12hr.second,
        microsecond=input_time_12hr.microsecond,
        tzinfo=input_time_12hr.tzinfo
    )

# Entry point: convert_12hr_to_24hr_time(input_time_12hr: time, is_pm: bool) -> time

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_22_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), bool_strategy())
def test_convert_12hr_to_24hr_time(input_time_12hr, is_pm):
    result = convert_12hr_to_24hr_time(input_time_12hr, is_pm)
    formatted_result = format_value_dt(result, input_time_12hr, is_pm)
    log_file.write(formatted_result + "\n")

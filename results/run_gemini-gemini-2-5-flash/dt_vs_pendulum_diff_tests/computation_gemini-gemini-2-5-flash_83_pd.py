
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_dst_end_date(year: int, timezone: pendulum.Timezone) -> pendulum.Date:
    # Step 1: Initialize a reference date at the beginning of the year in the given timezone.
    # We use noon to ensure we are not on the edge of a day boundary which might affect offset calculations
    # if the transition happens very early or late in the day.
    current_dt = pendulum.datetime(year, 1, 1, 12, 0, 0, tz=timezone)
    
    # Step 2: Get the initial UTC offset in minutes.
    # We will look for a decrease in this value to signify DST ending.
    previous_offset_minutes = current_dt.offset_minutes

    # Step 3: Iterate through the year, day by day, starting from January 1st.
    # DST typically ends in autumn, so we iterate until we find the change.
    # We can safely assume it will be found within the year.
    for _ in range(366): # Iterate up to 366 days to cover leap years
        # Move to the next day, keeping the same time of day (noon) and timezone.
        current_dt = current_dt.add(days=1)
        
        # Get the UTC offset for the current day.
        current_offset_minutes = current_dt.offset_minutes
        
        # Step 4: Check if the offset has decreased.
        # A decrease in offset_minutes (e.g., from -240 (EDT) to -300 (EST)) indicates DST ending.
        if current_offset_minutes < previous_offset_minutes:
            # Step 5: If a decrease is found, this is the day DST ended.
            # We need the date of the day *before* the offset changed to standard time
            # if we are looking for the day the clock *falls back*.
            # The `current_dt` already represents the day after the clock fell back,
            # so we should return the date of the previous day, which is when the clock adjustment effectively happens.
            # No, if `current_dt` has the *new, smaller* offset, it means the transition *happened* between `current_dt - 1 day` and `current_dt`.
            # Typically, DST ends at 2 AM on a Sunday, so the day itself is the day the clock falls back.
            # If current_dt is Monday 12PM, and its offset is smaller than Sunday 12PM, then DST ended on Sunday.
            # Let's consider `current_dt` (e.g., Monday). If its offset is smaller than `current_dt - 1 day` (e.g., Sunday),
            # then the DST end happened on Sunday.
            # So, `current_dt - 1 day` is the day we need.
            return current_dt.subtract(days=1).date()
        
        # Update the previous offset for the next iteration.
        previous_offset_minutes = current_offset_minutes
            
    # If the loop finishes without finding a DST end (e.g., in a timezone that doesn't observe DST
    # or for a year where DST is suspended, although pendulum handles standard transitions),
    # this part will be reached. For the purpose of this problem, we assume DST will end.
    # In a robust application, one might raise an error or return an optional type.
    # For simplicity, returning a default or raising an error if no transition found.
    # Assuming valid inputs will always lead to a transition for timezones that observe DST.
    raise ValueError(f"Could not find DST end date for year {year} in timezone {timezone.name}")


# Entry point: find_dst_end_date(year: int, timezone: pendulum.Timezone) -> pendulum.Date

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_83_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end_date(year, timezone):
    result = find_dst_end_date(year, timezone)
    formatted_result = format_value_pd(result, year, timezone)
    log_file.write(formatted_result + "\n")

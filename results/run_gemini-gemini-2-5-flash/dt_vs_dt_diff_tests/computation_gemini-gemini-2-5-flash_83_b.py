
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
def find_dst_end_date(year: int, tz: ZoneInfo) -> date:
    """
    Finds the date when daylight saving time ends for a given year and timezone.
    """
    
    # Start checking from a point where DST might still be active in either hemisphere,
    # and cover the period where it typically ends (e.g., from March to December).
    # We iterate day by day to find the exact date.
    
    # We'll use a `datetime` object to check the offset for each hour.
    # We initialize a datetime to the beginning of the year in the given timezone.
    dt_current = datetime(year, 1, 1, 0, 0, 0, tzinfo=tz)

    # Loop through the year, hour by hour, to detect the transition.
    # The maximum number of hours in a year is 366 days * 24 hours/day = 8784 hours.
    # We add a buffer to ensure we cover any edge cases.
    for _ in range(366 * 24 + 24): # Iterate for slightly more than a full year's hours
        dt_next_hour = dt_current + timedelta(hours=1)
        
        # Check if dt_current has a DST offset and dt_next_hour does not,
        # or if the UTC offset changes in a way that indicates DST ending.
        # DST ending means the local offset from UTC becomes 'more negative'
        # (e.g., UTC-4 becomes UTC-5), or equivalently, the dst() component goes to zero.
        
        # Compare the dst() component. When DST ends, this should transition from
        # a non-zero timedelta to a timedelta(0).
        if dt_current.tzinfo.dst(dt_current) > timedelta(0) and \
           dt_next_hour.tzinfo.dst(dt_next_hour) == timedelta(0):
            
            # This 'dt_next_hour' (or the hour *following* dt_current's standard time part)
            # is when the clocks have fallen back. The date of this transition is what we need.
            # The transition itself happens at dt_current's date (e.g., 2 AM becomes 1 AM again).
            return dt_current.date()
        
        dt_current = dt_next_hour

    # If no DST end is found (e.g., for a timezone that doesn't observe DST, or an error)
    # This scenario should not happen for a valid year and timezone that observes DST.
    # We could raise an error or return a specific indicator if needed, but per instructions,
    # we return a date. For non-DST zones, this loop won't find a transition.
    # For simplicity, and assuming input will always result in a DST end, this path is less likely.
    # If a timezone never observes DST, the condition will never be met.
    # To handle that, one might check if DST was ever active during the year.
    # For this problem, we assume a timezone that observes DST.
    
    # If we complete the loop without finding a transition, it implies DST might not
    # be observed for that year/timezone or the logic needs adjustment for extreme cases.
    # A safe fallback might be to indicate no DST end, but a specific date is expected.
    # As per prompt, we are looking for the *date* when DST *ends*.
    # If it never started, it never ended. This code finds the transition from DST active to inactive.
    
    # For a timezone that doesn't observe DST, this loop will finish without returning.
    # The prompt implies a timezone that *does* observe DST.
    # If a default is needed, it should be clarified. Given constraints,
    # we proceed assuming a transition will always be found for valid inputs.
    
    # If no transition is found, it means DST never applied or never ended.
    # A robust solution might return None or raise an exception in this case.
    # However, for this problem, we'll assume valid inputs where a DST end exists.
    # If the system requires a specific date for "no DST end", that needs clarification.
    # Let's consider a practical return for a year without DST end. For now, this will not return.
    # The prompt implies a valid DST-observing zone.

    # This line should ideally not be reached if DST is observed.
    # Returning a sentinel date for a case that shouldn't happen based on problem scope.
    return date(year, 1, 1) # Fallback, though a real DST transition should be found.

# Entry point: find_dst_end_date(year: int, tz: ZoneInfo) -> date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_83_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end_date(year, tz):
    result = find_dst_end_date(year, tz)
    formatted_result = format_value_dt(result, year, tz)
    log_file.write(formatted_result + "\n")

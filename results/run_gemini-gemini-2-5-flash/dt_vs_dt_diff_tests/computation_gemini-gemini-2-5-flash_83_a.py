
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def find_dst_end(year: int, tz: ZoneInfo) -> datetime:
    # DST typically ends in late autumn.
    # We'll check from October 1st up to mid-November to cover most common cases.
    # We will look for the first datetime when the offset changes from DST to standard.

    # Start checking from October 1st of the given year
    current_date = datetime(year, 10, 1, tzinfo=tz)

    # Iterate through days until we find the DST end
    while current_date.month <= 11: # Check up to end of November to be safe
        # Create a datetime object for 2 AM local time on the current day
        # We need to localize it explicitly to ensure the tzinfo is correctly applied
        # and to handle potential "fold" ambiguities.
        dt_local_2am = datetime(current_date.year, current_date.month, current_date.day, 2, 0, 0).replace(tzinfo=tz)
        
        # Check the UTC offset for 2 AM on the current day
        offset_current_day = dt_local_2am.utcoffset()

        # Compare with the UTC offset for 2 AM on the previous day
        dt_prev_day_2am = (current_date - timedelta(days=1)).replace(hour=2, tzinfo=tz)
        offset_prev_day = dt_prev_day_2am.utcoffset()

        # The end of DST is when the UTC offset becomes "more negative" (or less positive),
        # meaning the clock has "fallen back" to standard time.
        # This implies offset_current_day < offset_prev_day for typical timezones.
        # Or, more simply, when dst() returns timedelta(0) on the current day,
        # but was non-zero on the previous day.
        # Let's find the exact moment by iterating hours.
        
        # Check a specific hour that is usually affected by DST changes (e.g., 1 AM, 2 AM)
        # We check the hour before the transition and the hour after.
        # For example, if DST ends at 2 AM, we check 1:59 AM and 2:00 AM.
        # A more robust way is to check if the DST status *changes* from one hour to the next.
        
        # Let's get a datetime an hour before the typical transition time (e.g., 1 AM)
        dt_hour_before = datetime(current_date.year, current_date.month, current_date.day, 1, 0, 0).replace(tzinfo=tz)
        
        # Iterate through a few hours around the typical transition time (1 AM to 3 AM)
        for hour in range(1, 4): # Check 1 AM, 2 AM, 3 AM
            candidate_dt = datetime(current_date.year, current_date.month, current_date.day, hour, 0, 0).replace(tzinfo=tz)
            
            # Get the DST timedelta for the current candidate hour
            dst_timedelta = candidate_dt.dst()
            
            # Get the DST timedelta for the hour just before this candidate
            # We need to be careful with the fold attribute here.
            # A more direct approach is to check if an hour exists where fold=1.
            # When DST ends, a local time can occur twice (e.g., 1:30 AM EDT, then 1:30 AM EST).
            # The second occurrence will have fold=1 if it's explicitly generated.
            # The transition itself is the first local datetime *after* the DST offset is no longer applied.
            
            # Let's check the offset of the current minute and the previous minute
            # to pinpoint the exact moment of transition.
            # This is more precise. We iterate through minutes.
            
            # Start checking from 1 AM for the current day.
            test_dt = datetime(current_date.year, current_date.month, current_date.day, 1, 0, 0, tzinfo=tz)
            
            # A common DST end time is 2 AM or 3 AM local time.
            # Let's iterate minute by minute from 1 AM to 4 AM.
            for m_offset in range(3 * 60 + 1): # 3 hours and 1 minute (1 AM to 4 AM)
                test_moment = test_dt + timedelta(minutes=m_offset)
                
                # Check the DST status for this moment
                dst_at_moment = test_moment.dst()
                
                # Check the DST status for the moment one minute prior
                # We need to handle potential time zone ambiguities (fold=1).
                # The correct way to get the previous minute, considering fold, is crucial.
                prev_moment = test_moment - timedelta(minutes=1)
                
                # If we cross the boundary where DST was active and now it's not,
                # we have found the end of DST.
                # A more robust check: the UTC offset changes to the standard offset.
                # For example, if current offset is -04:00 (DST) and previous was -05:00 (Standard)
                # or current offset is -05:00 (Standard) and previous was -04:00 (DST).
                # We are looking for the transition from DST to standard.
                
                # Get naive datetime and localize it to get the correct fold.
                naive_test_moment = test_moment.replace(tzinfo=None)
                localized_test_moment = tz.localize(naive_test_moment)
                
                naive_prev_moment = prev_moment.replace(tzinfo=None)
                localized_prev_moment = tz.localize(naive_prev_moment)

                # The end of DST is detected when the current moment's DST offset is zero,
                # but the previous moment's DST offset was positive (e.g., 1 hour).
                if localized_test_moment.dst() == timedelta(0) and localized_prev_moment.dst() > timedelta(0):
                    # We found the transition point.
                    # The time returned should be the first moment that is NOT in DST.
                    # So, it's 'localized_test_moment'.
                    return localized_test_moment
            
        current_date += timedelta(days=1)
    
    # If DST end is not found within the checked range, which is unlikely for standard timezones.
    # This scenario should ideally not be reached for valid inputs.
    raise ValueError(f"Could not find DST end for year {year} in timezone {tz.key}")

# Entry point: find_dst_end(year: int, tz: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_83_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end(year, tz):
    result = find_dst_end(year, tz)
    formatted_result = format_value_dt(result, year, tz)
    log_file.write(formatted_result + "\n")

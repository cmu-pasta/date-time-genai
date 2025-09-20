
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_work_weeks(dt1: datetime, dt2: datetime) -> int:
    # Ensure dt1 is the earlier date and dt2 is the later date for consistent calculation
    start_date = min(dt1, dt2)
    end_date = max(dt1, dt2)

    # Find the Monday of the week for the start_date
    # weekday() returns 0 for Monday, 6 for Sunday
    days_until_monday_start = start_date.weekday()
    monday_of_start_week = start_date - timedelta(days=days_until_monday_start)

    # Find the Monday of the week for the end_date
    days_until_monday_end = end_date.weekday()
    monday_of_end_week = end_date - timedelta(days=days_until_monday_end)

    # Calculate the difference in days between these two Mondays
    # This effectively gives us the total number of full 7-day week spans.
    # Each full 7-day span represents one potential "work week" in this context.
    difference_in_days = (monday_of_end_week - monday_of_start_week).days

    # Divide by 7 to get the number of full weeks.
    # Use integer division to ensure an integer result.
    # If the dates are within the same calendar week, difference_in_days will be 0, resulting in 0 work weeks.
    # If end_date is Friday of Week 2 and start_date is Monday of Week 1,
    # monday_of_end_week - monday_of_start_week = 7 days, so 1 work week.
    # If end_date is Sunday of Week 2 and start_date is Monday of Week 1,
    # monday_of_end_week - monday_of_start_week = 7 days, so 1 work week.
    # If start_date is Monday of Week 1 and end_date is Sunday of Week 1,
    # monday_of_end_week - monday_of_start_week = 0 days, so 0 work weeks.
    # This logic gives the number of *full* 7-day periods between the *start of their respective weeks*.
    # A period like Monday-Friday within a single week will result in 0 full weeks between their Mondays.
    # To count the work week if the range spans it, we need to adjust.
    # The common interpretation of "weeks between two dates" often counts full week boundaries.
    # Let's refine for "work weeks". A work week is Mon-Fri.

    # Re-evaluate for "work weeks".
    # We want to count how many distinct Mon-Fri periods are touched or fully contained.
    # A simpler approach: Count the number of full 7-day periods *starting from* the Monday of the start_date's week.
    # This gives us the number of *calendar* weeks that *begin* within the interval.
    # Example: Mon Jan 1 (W1) to Fri Jan 5 (W1) -> monday_of_start = Mon Jan 1, monday_of_end = Mon Jan 1. diff = 0.
    # Example: Mon Jan 1 (W1) to Mon Jan 8 (W2) -> monday_of_start = Mon Jan 1, monday_of_end = Mon Jan 8. diff = 7. Weeks = 1.
    # This means 1 *full* Monday-Sunday period has elapsed.

    # To count "work weeks" it's often the number of distinct Mon-Fri spans encountered.
    # The simplest way to count weeks between dates (regardless of work/calendar) is to find the number of full week intervals.
    # We can adjust the start_date to the beginning of its week (Monday) and end_date to the end of its week (Sunday)
    # or just use the difference in Mondays.

    # Let's count the number of Mondays in the range including the start date's Monday
    # and up to (but not including) the end date's Monday, then add 1 if the end date falls into a new week.
    
    # Let's stick to the interpretation of "how many Monday-Friday periods exist in the span".
    # This implies counting how many full 7-day week *boundaries* are crossed.
    # If start_date = Mon, end_date = Fri (same week), result should be 0 (no full week boundary crossed after the start).
    # If start_date = Mon (Week 1), end_date = Mon (Week 2), result should be 1 (one full week boundary crossed).

    # The difference between the Monday of the week of `end_date` and the Monday of the week of `start_date`,
    # divided by 7, gives the number of *full* 7-day intervals between these Mondays.
    # For example, if start is Jan 1 (Mon) and end is Jan 5 (Fri), both Mondays are Jan 1. Diff is 0. Result 0.
    # If start is Jan 1 (Mon) and end is Jan 8 (Mon), start_monday=Jan 1, end_monday=Jan 8. Diff is 7. Result 1.
    # If start is Jan 1 (Mon) and end is Jan 12 (Fri), start_monday=Jan 1, end_monday=Jan 8. Diff is 7. Result 1. This isn't right.
    # It should be 2 work weeks for Jan 1-5 and Jan 8-12.

    # A more robust approach for "number of weeks spanned":
    # Calculate the difference in weeks by looking at the week number (ISO week number) or by
    # counting the number of Mondays.

    # To calculate number of *work weeks spanned*:
    # 1. Adjust start_date to the beginning of its work week (Monday) if it's not already.
    # 2. Adjust end_date to the end of its work week (Friday) if it's not already.
    # 3. Then calculate the number of full weeks.

    # Let's calculate the difference in days.
    total_days = (end_date - start_date).days

    # A work week is 5 days (Mon-Fri). A calendar week is 7 days.
    # The simplest interpretation for "number of work weeks" often relates to how many
    # Monday-Sunday periods are partially or fully included, where each such period counts as one "work week" if it has workdays.

    # Let's find the ISO week number for both dates.
    # isoformat() returns (year, week, weekday) where weekday is 1=Mon, ..., 7=Sun.
    # This simplifies week counting.

    # If the year is different, just subtracting week numbers isn't enough.
    # We need to normalize to a common start point, e.g., the Monday of the week.

    # Consider the start and end of the full range.
    # Find the Monday of the first week that contains a workday from the range.
    # Find the Monday of the last week that contains a workday from the range.
    # The difference between these Mondays, divided by 7, gives the number of work weeks.

    # Example: dt1 = 2024-01-01 (Mon), dt2 = 2024-01-05 (Fri)
    # Mon of dt1 week = 2024-01-01
    # Mon of dt2 week = 2024-01-01
    # Difference = 0 days. Result = 0? This isn't right. This should be 1 work week.

    # It seems the prompt is asking for the number of *distinct* Monday-Friday spans that are intersected by the date range.
    # This is equivalent to counting the number of distinct Mondays that fall within or define the start of the week for the range.

    # Let's re-interpret: count the number of full or partial Monday-Friday work weeks that occur between dt1 and dt2.
    # This means if dt1 is Monday and dt2 is Tuesday *in the same week*, it's 1 work week.
    # If dt1 is Friday and dt2 is Monday of the *next* week, it's 2 work weeks.

    # Step 1: Normalize start_date to the Monday of its week.
    # Step 2: Normalize end_date to the Monday of its week, BUT only if end_date is not already a Monday.
    #         If end_date is a Monday, it signifies the start of a *new* week.
    
    # Calculate days from Monday (0 is Monday)
    start_monday = start_date - timedelta(days=start_date.weekday())
    end_monday = end_date - timedelta(days=end_date.weekday())

    # If the end_date itself is a Monday, and it's not the same Monday as start_monday,
    # it represents the beginning of a new work week that should be counted.
    # The calculation (end_monday - start_monday).days // 7 naturally counts full week boundaries.
    # Example: start = Mon 1, end = Fri 5. start_monday = Mon 1, end_monday = Mon 1. diff = 0.
    # Example: start = Mon 1, end = Mon 8. start_monday = Mon 1, end_monday = Mon 8. diff = 7. Result = 1.
    # This is counting the number of *full* 7-day periods that have *passed* between the starts of the weeks.

    # A better approach for "number of work weeks" (as commonly understood for range spanning):
    # Find the week number of the first date, and the week number of the second date.
    # If using ISO week numbers, these are numbers from 1 to 52/53.
    # datetime.isocalendar() returns (year, week, weekday)

    # Consider the period from the Monday of the start date's week up to the Monday of the end date's week.
    # If start_date is Friday, Jan 5, 2024. end_date is Monday, Jan 8, 2024.
    # start_monday = Jan 1, end_monday = Jan 8.
    # (Jan 8 - Jan 1).days = 7. 7 // 7 = 1. This would mean 1 work week, which is incorrect. It should be 2.

    # A work week is a Monday-Friday period. We need to count how many such periods the interval [dt1, dt2] overlaps.
    # Let's define the start of the "work week period" as the Monday of `dt1`'s week.
    # Let's define the end of the "work week period" as the Sunday of `dt2`'s week.
    # This creates a range of full calendar weeks.
    
    # Get the Monday of the week for start_date (adjusting for earlier dates if necessary)
    monday_of_start = start_date - timedelta(days=start_date.weekday())
    # Get the Sunday of the week for end_date
    sunday_of_end = end_date + timedelta(days=6 - end_date.weekday())

    # Now, calculate the total number of days in this full weekly span
    total_span_days = (sunday_of_end - monday_of_start).days + 1

    # Divide by 7 to get the number of full calendar weeks spanned.
    # Each full calendar week contains exactly one potential work week (Mon-Fri).
    num_calendar_weeks_spanned = total_span_days // 7
    
    return num_calendar_weeks_spanned

# Entry point: calculate_work_weeks(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_57_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_work_weeks(dt1, dt2):
    result = calculate_work_weeks(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")

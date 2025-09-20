
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time, timedelta, timezone
def calculate_working_hours_between(dt_start: datetime, dt_end: datetime) -> float:
    # Ensure chronological order
    if dt_start > dt_end:
        dt_start, dt_end = dt_end, dt_start

    # If both are timezone-aware, normalize to UTC for consistent day boundaries
    if (dt_start.tzinfo is not None and dt_start.tzinfo.utcoffset(dt_start) is not None) and \
       (dt_end.tzinfo is not None and dt_end.tzinfo.utcoffset(dt_end) is not None):
        dt_start = dt_start.astimezone(timezone.utc)
        dt_end = dt_end.astimezone(timezone.utc)

    # Business hours: 09:00 to 17:00 (8 hours)
    biz_start_t = time(9, 0, 0)
    biz_end_t = time(17, 0, 0)

    # Helper to build a datetime with the same tzinfo as the provided datetime
    def at_time(d: datetime, t: time) -> datetime:
        return datetime(d.year, d.month, d.day, t.hour, t.minute, t.second, t.microsecond, tzinfo=d.tzinfo)

    total_seconds = 0.0

    # Iterate over days
    current_day = datetime(dt_start.year, dt_start.month, dt_start.day, tzinfo=dt_start.tzinfo)
    end_day = datetime(dt_end.year, dt_end.month, dt_end.day, tzinfo=dt_end.tzinfo)

    # We will loop until we pass the date part of dt_end
    days = (end_day.date() - current_day.date()).days
    for i in range(days + 1):
        day = current_day + timedelta(days=i)

        # Skip weekends: Saturday=5, Sunday=6
        if day.weekday() >= 5:
            continue

        day_start = at_time(day, biz_start_t)
        day_end = at_time(day, biz_end_t)

        # Compute overlap between [day_start, day_end] and [dt_start, dt_end]
        start_overlap = max(day_start, dt_start)
        end_overlap = min(day_end, dt_end)

        if end_overlap > start_overlap:
            total_seconds += (end_overlap - start_overlap).total_seconds()

    # Convert seconds to hours
    return total_seconds / 3600.0

# Entry point: calculate_working_hours_between(dt_start: datetime, dt_end: datetime) -> float

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_24_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours_between(dt_start, dt_end):
    result = calculate_working_hours_between(dt_start, dt_end)
    formatted_result = format_value_dt(result, dt_start, dt_end)
    log_file.write(formatted_result + "\n")

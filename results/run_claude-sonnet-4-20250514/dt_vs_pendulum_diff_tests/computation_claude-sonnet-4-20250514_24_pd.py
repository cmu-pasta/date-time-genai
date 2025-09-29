
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_working_hours_excluding_weekends(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> float:
    # Ensure dt1 is the earlier datetime
    start_dt = min(dt1, dt2)
    end_dt = max(dt1, dt2)
    
    if start_dt.date() == end_dt.date():
        # Same day calculation
        if start_dt.weekday() in [6, 7]:  # Weekend (Saturday=6, Sunday=7)
            return 0.0
        else:
            return (end_dt - start_dt).total_seconds() / 3600.0  # Convert to hours
    
    total_working_hours = 0.0
    current_date = start_dt.date()
    
    while current_date <= end_dt.date():
        current_weekday = pendulum.parse(str(current_date)).weekday()
        
        # Skip weekends (Saturday=6, Sunday=7)
        if current_weekday in [6, 7]:
            current_date = current_date.add(days=1)
            continue
        
        if current_date == start_dt.date():
            # First day - from start_dt to end of day or end_dt if same day
            if current_date == end_dt.date():
                # Same day, already handled above
                break
            else:
                end_of_day = pendulum.parse(str(current_date)).end_of('day')
                total_working_hours += (end_of_day - start_dt).total_seconds() / 3600.0
        elif current_date == end_dt.date():
            # Last day - from start of day to end_dt
            start_of_day = pendulum.parse(str(current_date)).start_of('day')
            total_working_hours += (end_dt - start_of_day).total_seconds() / 3600.0
        else:
            # Full day - 24 hours
            total_working_hours += 24.0
        
        current_date = current_date.add(days=1)
    
    return total_working_hours

# Entry point: calculate_working_hours_excluding_weekends(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> float

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_24_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours_excluding_weekends(dt1, dt2):
    result = calculate_working_hours_excluding_weekends(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")

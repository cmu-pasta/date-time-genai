
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
import random
def generate_random_date_within_range(start_date: date, end_date: date) -> date:
    # Step 1: Ensure start_date <= end_date for correct range calculation
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Step 2: Calculate the number of days between the dates
    days_range = (end_date - start_date).days
    
    # Step 3: Generate a random integer within the range [0, days_range]
    random_days = random.randint(0, days_range)
    
    # Step 4: Add the random number of days to the start_date
    random_date = start_date + timedelta(days=random_days)
    
    # Step 5: Return the generated date
    return random_date

# Entry point: generate_random_date_within_range(start_date: date, end_date: date) -> date

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_17txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_generate_random_date_within_range(start_date, end_date):
    result = generate_random_date_within_range(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")

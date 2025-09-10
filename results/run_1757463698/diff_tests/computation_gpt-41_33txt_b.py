
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def is_us_federal_holiday(dt: date) -> bool:
    year = dt.year

    # Fixed date holidays
    new_years = date(year, 1, 1)
    independence_day = date(year, 7, 4)
    veterans_day = date(year, 11, 11)
    christmas = date(year, 12, 25)

    # Helper for Sunday/Monday shifting (observed holidays)
    def observed(day: date):
        if day.weekday() == 5:      # Saturday
            return day - timedelta(days=1)
        elif day.weekday() == 6:    # Sunday
            return day + timedelta(days=1)
        else:
            return day

    # Martin Luther King Jr. Day: Third Monday in January
    mlk_day = date(year, 1, 1) + timedelta(days=(14 - date(year, 1, 1).weekday()) % 7 + 14)

    # Washington's Birthday (Presidents Day): Third Monday in February
    presidents_day = date(year, 2, 1) + timedelta(days=(14 - date(year, 2, 1).weekday()) % 7 + 14)

    # Memorial Day: Last Monday in May
    last_day_may = date(year, 5, 31)
    memorial_day = last_day_may - timedelta(days=last_day_may.weekday())

    # Juneteenth: June 19
    juneteenth = date(year, 6, 19)

    # Labor Day: First Monday in September
    labor_day = date(year, 9, 1) + timedelta(days=(0 - date(year, 9, 1).weekday()) % 7)

    # Columbus Day: Second Monday in October
    columbus_day = date(year, 10, 1) + timedelta(days=(7 - date(year, 10, 1).weekday()) % 7 + 7)

    # Veterans Day (observed if on weekend)
    veterans_day_observed = observed(veterans_day)

    # Thanksgiving: Fourth Thursday in November
    thanksgiving = date(year, 11, 1) + timedelta(days=((3 - date(year, 11, 1).weekday()) % 7) + 21)

    # Christmas (observed if on weekend)
    christmas_observed = observed(christmas)

    # New Year's (observed if on weekend)
    new_years_observed = observed(new_years)

    # Independence Day (observed if on weekend)
    independence_day_observed = observed(independence_day)
    
    # Juneteenth (observed if on weekend)
    juneteenth_observed = observed(juneteenth)

    # Build set of actual and observed holiday dates
    holidays = {
        new_years, new_years_observed,
        mlk_day,
        presidents_day,
        memorial_day,
        juneteenth, juneteenth_observed,
        independence_day, independence_day_observed,
        labor_day,
        columbus_day,
        veterans_day, veterans_day_observed,
        thanksgiving,
        christmas, christmas_observed
    }

    return dt in holidays

# Entry point: is_us_federal_holiday(dt: date) -> bool

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_33txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_is_us_federal_holiday(dt):
    result = is_us_federal_holiday(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")

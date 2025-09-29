from datetime import date, datetime, timedelta
from zoneinfo import available_timezones

import pendulum
from hypothesis import strategies as st


@st.composite
def datetime_strategy(draw):
    # Generate a datetime within reasonable bounds
    dt = draw(
        st.datetimes(min_value=datetime(1900, 1, 1), max_value=datetime(2100, 12, 31))
    )
    # Create equivalent Pendulum datetime
    pd_dt = pendulum.datetime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
    )
    return pd_dt


@st.composite
def date_strategy(draw):
    # Generate a date within reasonable bounds
    dt_date = draw(st.dates(min_value=date(1900, 1, 1), max_value=date(2100, 12, 31)))
    # Create equivalent Pendulum date
    pd_date = pendulum.date(dt_date.year, dt_date.month, dt_date.day)
    return pd_date


@st.composite
def time_strategy(draw):
    # Generate a time
    dt_time = draw(st.times())
    # Create equivalent Pendulum time
    pd_time = pendulum.time(
        dt_time.hour, dt_time.minute, dt_time.second, dt_time.microsecond
    )
    return pd_time


@st.composite
def duration_strategy(draw):
    # Generate a timedelta
    days = draw(st.integers(min_value=0, max_value=365))
    hours = draw(st.integers(min_value=0, max_value=23))
    minutes = draw(st.integers(min_value=0, max_value=59))
    seconds = draw(st.integers(min_value=0, max_value=59))

    dt_delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    pd_duration = pendulum.duration(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    )

    return pd_duration


@st.composite
def timestamp_strategy(draw):
    # Generate a datetime
    dt = draw(
        st.datetimes(min_value=datetime(1900, 1, 1), max_value=datetime(2100, 12, 31))
    )
    # Convert to integer timestamp (seconds since epoch)
    ts_int = int(dt.timestamp())
    # Create a Pendulum datetime from that timestamp
    pd_dt = pendulum.from_timestamp(ts_int)
    return pd_dt


@st.composite
def string_strategy(draw):
    # Generate a string value.
    s = draw(st.text())
    return s


@st.composite
def bool_strategy(draw):
    # Generate a boolean value.
    b = draw(st.booleans())
    return b


@st.composite
def float_strategy(draw):
    # Generate a float value within a reasonable range.
    f = draw(
        st.floats(
            min_value=-1e10, max_value=1e10, allow_nan=False, allow_infinity=False
        )
    )
    return f


@st.composite
def timezone_strategy(draw):
    """
    Hypothesis strategy that yields pendulum.Timezone instances
    from the full set of IANA timezones available in zoneinfo.
    """
    tz_names = sorted(available_timezones())
    tz_name = draw(st.sampled_from(tz_names))
    return pendulum.timezone(tz_name)

from datetime import datetime, timedelta, timezone
from dateutil import parser

UTC_OFFSET: timedelta = datetime.utcnow() - datetime.now()
"""Local time + UTC_OFFSET = UTC Time"""

def parse_to_utc(date_string: str) -> datetime:
    """
    Parse a date string to UTC time.
    """
    raw_datetime = parser.parse(date_string) + UTC_OFFSET
    datetime_utc = raw_datetime.replace(tzinfo=timezone.utc)
    return datetime_utc

def parse_to_local(datetime_utc: datetime) -> datetime:
    """
    Parse a datetime object to local time.
    """
    return datetime_utc.astimezone()

TODAY_UTC: datetime = parse_to_utc(datetime.today().strftime('%Y-%m-%d'))
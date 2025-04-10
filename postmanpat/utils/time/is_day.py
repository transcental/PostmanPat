from datetime import datetime
from typing import cast

import pytz
from astral import LocationInfo
from astral.geocoder import database
from astral.geocoder import lookup
from astral.sun import sun


def is_day(city: str) -> bool:
    try:
        location = cast(LocationInfo, lookup(city, database()))
    except KeyError:
        location = cast(LocationInfo, lookup("London", database()))

    timezone = pytz.timezone(location.timezone)
    now = datetime.now(timezone)
    s = sun(location.observer, date=now, tzinfo=timezone)

    return s["sunrise"] < now < s["sunset"]

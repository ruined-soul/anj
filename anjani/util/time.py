"""Anjani time utils"""
# Copyright (C) 2020 - 2022  UserbotIndo Team, <https://github.com/userbotindo.git>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from typing import Union


def usec() -> int:
    """Returns the current time in microseconds since the Unix epoch."""

    return int(time.time() * 1000000)


def msec() -> int:
    """Returns the current time in milliseconds since the Unix epoch."""

    return int(usec() / 1000)


def sec() -> int:
    """Returns the current time in seconds since the Unix epoch."""

    return int(time.time())


def format_duration_us(t_us: Union[int, float]) -> str:
    """Formats the given microsecond duration as a string."""

    t_us = int(t_us)

    t_ms = t_us / 1000
    t_s = t_ms / 1000
    t_m = t_s / 60
    t_h = t_m / 60
    t_d = t_h / 24

    if t_d >= 1:
        rem_h = t_h % 24
        return "%dd %dh" % (t_d, rem_h)

    if t_h >= 1:
        rem_m = t_m % 60
        return "%dh %dm" % (t_h, rem_m)

    if t_m >= 1:
        rem_s = t_s % 60
        return "%dm %ds" % (t_m, rem_s)

    if t_s >= 1:
        return "%d sec" % t_s

    if t_ms >= 1:
        return "%d ms" % t_ms

    return "%d μs" % t_us


def extract_time(time_text: str) -> Union[int, bool]:
    """Extract time from time flags"""
    if any(time_text.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_text[-1]
        time_num = time_text[:-1]
        if not time_num.isdigit():
            return False

        if unit == "m":
            return int(time.time() + int(time_num) * 60)

        if unit == "h":
            return int(time.time() + int(time_num) * 60 * 60)

        if unit == "d":
            return int(time.time() + int(time_num) * 24 * 60 * 60)

    return False

"""Logging setup"""
# Copyright (C) 2020 - 2021  UserbotIndo Team, <https://github.com/userbotindo.git>
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
import logging
from datetime import datetime

import colorlog


def setup_log():
    """Configures logging"""
    level = logging.INFO
    file_path = f"anjani_bot/core/AnjaniBot-{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.root.setLevel(level)

    # Logging into file
    file_format = "[ %(asctime)s: %(levelname)-7s ] %(name)-31s - %(message)s"
    logfile = logging.FileHandler(file_path)
    formatter = logging.Formatter(file_format, datefmt="%H:%M:%S")
    logfile.setFormatter(formatter)
    logfile.setLevel(level)

    # Logging into stderr with color
    term_format = (
        "  %(bold)s%(asctime)s%(reset)s: "
        "%(log_color)s%(levelname)-7s%(reset)s | %(name)-31s - "
        "%(log_color)s%(message)s%(reset)s"
    )
    stream = logging.StreamHandler()
    formatter = colorlog.ColoredFormatter(term_format, datefmt="%H:%M:%S")
    stream.setLevel(level)
    stream.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(logfile)
    root.addHandler(stream)

    logging.getLogger("pyrogram").setLevel(logging.WARNING)

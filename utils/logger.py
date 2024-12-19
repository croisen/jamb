from pathlib import Path
from typing import IO
import datetime
import logging
import os
import sys


def supports_color(stream: IO[str]) -> bool:
    tty = hasattr(stream, "isatty") and stream.isatty()
    return tty


class ColorFormat(logging.Formatter):
    level_colours = [
        (logging.DEBUG, "\x1b[40;1m"),
        (logging.INFO, "\x1b[34;1m"),
        (logging.WARNING, "\x1b[33;1m"),
        (logging.ERROR, "\x1b[31m"),
        (logging.CRITICAL, "\x1b[41m"),
    ]

    formats = {
        level: logging.Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        for level, colour in level_colours
    }

    def format(self, record: logging.LogRecord) -> str:
        formatter: logging.Formatter = self.formats.get(record.levelno)
        if formatter is None:
            formatter = self.formats[logging.DEBUG]

        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)
        record.exc_text = None
        return output


def setup_logging(log_dir: Path) -> None:
    if not (log_dir.exists() and log_dir.is_dir()):
        log_dir.mkdir()

    dt_fmt = "%Y-%m-%d %H:%M:%S"
    stdout = logging.StreamHandler(sys.stdout)
    stdout_formatter = None
    file = logging.FileHandler(log_dir / f"{datetime.date.today()}.log", "a", "utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s %(message)s", dt_fmt
    )

    if supports_color(stdout.stream):
        stdout_formatter = ColorFormat()
    else:
        stdout_formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(name)s %(message)s", dt_fmt
        )

    root_logger = logging.getLogger()
    stdout.setFormatter(stdout_formatter)
    file.setFormatter(file_formatter)
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(stdout)
    root_logger.addHandler(file)

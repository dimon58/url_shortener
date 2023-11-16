from pathlib import Path

DEBUG = False
BASE_DIR = Path(__file__).resolve().parent

BASE_URL = ""

DB_URL = "sqlite+aiosqlite:///db.sqlite3"
URL_LENGTH = 6  # 62**6 = 56800235584 unique urls

LOGGING_FOLDER = BASE_DIR / "logs"
LOGGING_FOLDER.mkdir(exist_ok=True)
LOG_FILE = LOGGING_FOLDER / "logs.log"
LOGGING_FORMAT = "[%(name)s:%(filename)s:%(funcName)s:%(lineno)d:%(asctime)s:%(levelname)s] %(message)s"
LOGGING_DATE_FORMAT = "%d-%m-%Y %H:%M:%S"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": LOGGING_FORMAT,
            "datefmt": LOGGING_DATE_FORMAT,
        },
        "colored": {
            "()": "coloredlogs.ColoredFormatter",
            "format": LOGGING_FORMAT,
            "datefmt": LOGGING_DATE_FORMAT,
            "field_styles": {
                "asctime": {"color": "green"},
                "hostname": {"color": "magenta"},
                "name": {"color": "blue"},
                "programname": {"color": "cyan"},
                "username": {"color": "yellow"},
            },
        },
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": LOG_FILE,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["stream_handler", "file_handler"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": True,
            "encoding": "utf-8",
        },
        "sqlalchemy.engine": {
            "level": "DEBUG" if DEBUG else "WARNING",
        },
    },
}

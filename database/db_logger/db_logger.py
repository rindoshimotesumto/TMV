from datetime import datetime

LOG_FILE = "database/db_logger/database.log"

def _write(line: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def db_ok(operation: str):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _write(f"{t} | {operation}")

def db_error(error: Exception):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _write(f"{t} | {error}")
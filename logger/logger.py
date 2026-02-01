from datetime import datetime

HANDLERS_LOG_FILE = ".log"


def _write(line: str):
    with open(HANDLERS_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def write_logs(log: str):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _write(f"{t} | {log}")

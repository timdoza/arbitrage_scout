from datetime import datetime
import os

LOG_FILE = "request_log.txt"

def log_request(query: str, success: bool, error: str = None):
    """
    Records each eBay API call with timestamp, query, and success/error info.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    message = f"[{timestamp}] {status} | query='{query}'"
    if error:
        message += f" | error='{error}'"
    message += "\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message)

    # optional: print to console for quick visibility
    print(message.strip())

def count_requests_today():
    """
    Returns the number of logged requests made today.
    """
    if not os.path.exists(LOG_FILE):
        return 0
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(f"[{today}]"):
                count += 1
    return count
import csv
from datetime import datetime

def count_agent_usage(func):
    def wrapper(*args, **kwargs):
        today = datetime.now().strftime("%Y-%m-%d")
        with open("agent_usage.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([today,1])
        return func(*args, **kwargs)
    return wrapper

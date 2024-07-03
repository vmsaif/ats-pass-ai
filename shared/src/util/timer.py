import time
from datetime import timedelta

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start

def print_task_time(task_name, total_seconds):
    days, hours, minutes, seconds = convert_seconds(total_seconds)
    print(f"-- Time taken for {task_name}: {minutes} minutes, {seconds} seconds")

def convert_seconds(total_seconds):
    # Extract days, seconds from timedelta
    td = timedelta(seconds=total_seconds)
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format each component to two decimal places
    formatted_days = f"{days:.2f}"
    formatted_hours = f"{hours:.2f}"
    formatted_minutes = f"{minutes:.2f}"
    formatted_seconds = f"{seconds:.2f}"
    
    return formatted_days, formatted_hours, formatted_minutes, formatted_seconds

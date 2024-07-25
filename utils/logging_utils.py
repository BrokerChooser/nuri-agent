from datetime import datetime


def log_to_output(text):
    """Log to the console with a timestamp"""

    curr_time = datetime.now()
    dt_string = curr_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{dt_string}]: {text}")


import json
import time
from datetime import datetime


def print_current_time():
    try:
        while True:
            current_time = datetime.now().strftime("%H:%M:%S:%f")[:-3]
            waybar_json = [{"text": current_time, "class": "custom-widget"}]
            print(json.dumps(waybar_json), flush=True)

            # Sleep for 1 millisecond
            time.sleep(0.001)

    except KeyboardInterrupt:
        # Print an empty JSON array when interrupted (e.g., Ctrl+C)
        print("[]", flush=True)


# Call the function to continuously print the current time in Waybar-compatible JSON format
print_current_time()

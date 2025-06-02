import threading
import time
import requests

def ping_periodically():
    while True:
        try:
            # Replace with your actual URL or use localhost if accessible
            response = requests.get("https://commerce-0in7.onrender.com/ping/")
            response = requests.get("http://127.0.0.1:8000/ping/")
            print(f"Ping response status: {response.status_code}")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(1 * 60)  # Sleep 12 minutes
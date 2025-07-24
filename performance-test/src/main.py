from base64 import b64decode
from json import loads
from os import system

import functions_framework


@functions_framework.cloud_event
def perf_test_support_agent(cloud_event):
    """
    Cloud Function to handle performance testing for the support agent.
    """
    try:
        # Decode the base64-encoded data from the Cloud Event
        data = b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
        payload = loads(data)

        # Log the received payload
        print(f"Received payload: {payload}")

        locust_time = payload.get("locust_time", 1)
        locust_users = payload.get("locust_users", 1)
        locust_spawn_rate = payload.get("locust_spawn_rate", 1)

        cmd = f"locust -f performance_test_script.py --headless -u {locust_users} -r {locust_spawn_rate} -t {locust_time}s --host http://localhost:8000"
        print(f"Executing command: {cmd}")
        system(cmd)
    except Exception as e:
        print(f"Error processing Cloud Event: {e}")
        raise e

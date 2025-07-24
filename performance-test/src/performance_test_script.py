import os
import time
from random import choice
from uuid import uuid4

import requests
import requests.adapters
from locust import HttpUser, events, task
from test_data import queries

requests.adapters.DEFAULT_RETRIES = 0


class CustomHTTPAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections=10, maxsize=10, block=False, **pool_kwargs):
        self.poolmanager = requests.adapters.PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, **pool_kwargs
        )


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    Listener to set up the HTTP adapter for the environment.
    """
    print("Load test started..")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Listener to close the HTTP session when the test stops.
    """
    print("Load test ended..")


class SupportAgentUser(HttpUser):
    """
    User class for Locust to simulate requests to the support agent endpoint.
    """

    @task
    def predict(self):
        """
        Task to send a prediction request to the support agent endpoint.
        """
        session = requests.sessions.Session()
        adapter = CustomHTTPAdapter(max_retries=0)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        query = choice(queries)
        payload = {"query": query, "query_id": str(uuid4()), "session_id": str(uuid4())}
        test_url = os.getenv("test_url", "http://")
        api_start_time = time.time()
        response = self.client.post(test_url, json=payload, headers=None)
        print(f"API Latency in seconds: {time.time() - api_start_time:.2f}")
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")

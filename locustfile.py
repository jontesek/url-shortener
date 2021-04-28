import os
import random
import string
import time

from locust import HttpUser, constant, task

CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase


class QuickstartUser(HttpUser):
    # wait_time = constant(0.1)
    host = "http://0.0.0.0:8080"
    urls_dir = "s3_storage/shortener/urls/"

    def _generate_long_url(self):
        _r_string = "".join(
            [random.choice(CHARS) for _ in range(random.randint(10, 20))]
        )
        return f"https://{_r_string}.com"

    # @task
    def shorten(self):
        url = self._generate_long_url()
        self.client.get(f"/shorten?url={url}")

    @task
    def redirect(self):
        url_id = random.choice(self.url_ids)
        self.client.get(f"/{url_id}")

    def on_start(self):
        self.url_ids = os.listdir(self.urls_dir)[:1000]

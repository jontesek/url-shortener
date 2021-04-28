import asyncio
import concurrent.futures
import functools
from typing import Optional

import botocore

# Define async behaviour.
executor = concurrent.futures.ThreadPoolExecutor()


def aio(func):
    async def aio_wrapper(**kwargs):
        f_bound = functools.partial(func, **kwargs)
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, f_bound)

    return aio_wrapper


class S3Client:
    def __init__(self, client, bucket: str, url_path: str) -> None:
        self.client = client
        self.bucket = bucket
        self.url_path = url_path
        # You can comment this once bucket is created.
        self._check_if_bucket_exists()
        # Create async methods.
        self._get_object = aio(self.client.get_object)
        self._put_object = aio(self.client.put_object)

    def _check_if_bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except botocore.client.ClientError:
            self.client.create_bucket(Bucket=self.bucket)

    async def save_url(self, url_id: str, long_url: str) -> str:
        key = f"{self.url_path}{url_id}"
        await self._put_object(Body=long_url.encode(), Bucket=self.bucket, Key=key)
        return key

    async def get_url(self, url_id: str) -> Optional[str]:
        key = f"{self.url_path}{url_id}"
        try:
            obj = await self._get_object(Bucket=self.bucket, Key=key)
        except self.client.exceptions.NoSuchKey:
            return None
        return obj["Body"].read().decode()

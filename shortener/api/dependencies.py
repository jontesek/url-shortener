import aioredis
import boto3

from ..clients.s3 import S3Client
from ..settings import REDIS_URL, S3_BUCKET, S3_CONFIG, URL_S3_PATH
from ..shortener import Shortener

# pylint: disable=invalid-name
shortener = None


async def get_shortener() -> Shortener:
    global shortener
    if not shortener:
        print("creating shortener")
        _redis_client = await aioredis.create_redis_pool(REDIS_URL, encoding="utf-8")
        _boto_client = boto3.client(
            "s3",
            endpoint_url=S3_CONFIG["endpoint"],
            aws_access_key_id=S3_CONFIG["access_key"],
            aws_secret_access_key=S3_CONFIG["secret_key"],
        )
        _s3_client = S3Client(
            client=_boto_client, bucket=S3_BUCKET, url_path=URL_S3_PATH
        )
        shortener = Shortener(redis=_redis_client, s3=_s3_client)
    return shortener

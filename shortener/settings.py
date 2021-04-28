import os

# Config
S3_CONFIG = {
    "endpoint": os.getenv("S3_ENDPOINT"),
    "access_key": os.getenv("S3_ACCESS_KEY"),
    "secret_key": os.getenv("S3_SECRET_KEY"),
}
S3_BUCKET = os.getenv("S3_BUCKET", "shortener")
REDIS_URL = os.getenv("REDIS_URL")
REDIRECT_BASE_URL = os.getenv("REDIRECT_BASE_URL", "http://localhost:8080")
SENTRY_DSN = os.getenv("SENTRY_DSN")
DD_HOSTNAME = os.getenv("DD_HOSTNAME")
DD_TRACER_PORT = os.getenv("DD_TRACER_PORT", "8126")
APP_NAME = os.getenv("APP_NAME", "shortener")
ENVIRONMENT = os.getenv("ENVIRONMENT")
DEBUG = os.getenv("DEBUG")

local = ENVIRONMENT == "local"

# Constants
URL_REGEX = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)$"
URL_ID_REGEX = r"^[a-zA-Z0-9]+$"
KEY_COUNTER = "counter"
KEY_URL_ID = "id"
URL_CACHE_SECONDS = 86400  # 24 hours
URL_S3_PATH = "urls/"

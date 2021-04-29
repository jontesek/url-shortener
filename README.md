# Concurrent URL shortener

## Installation and usage

1. `mkdir s3_storage`
2. `touch .env`
3. `docker-compose up`

The service is then accessible on URL `http://0.0.0.0:8080` and you can use two endpoints:

* GET `/shorten?url=<url>`: generate short URL
    * example: `http://0.0.0.0:8080/shorten?url=https://www.engadget.com/ps5-sales-tma-113435891.html`
* GET `/<url_id>`: get long URL (if service deployed for real, redirect would happen)
    * example: `http://localhost:8080/sV21`

More details are available in the generated [Swagger docs](http://0.0.0.0:8080/docs).

## Description

### My premises

* CPU time is cheap
* Redis is super fast
* Key-value DB is fast and scalable
* SQL DB is slow and unscalable

### Architecture

* Permanent storage: S3 bucket (locally server by `minio` server)
* Cache: Redis instance
* Access: HTTP API
* Logging: `structlog` 
* Monitoring: Datadog APM, Sentry
* Metrics: none - can be added via `statsd` and seen in Datadog

App structure:
* Main logic: `/shortener/shortener.py` ->
* API endpoints: `/shortener/api/routers`, they access the globally created Shortener object (see `/shortener/api/dependencies.py`).
* Tests: unit tests for `url_id.py` in `test` folder
* Logs: a simple config defined in `shortener/__init__.py`

### Algorithm for URL shortening

We store a decimal integer counter. This counter is incremented by one for each new shortened URL. The new value is then converted to a base62 number. We than map the digits to corresponding characters based on this list:

`0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`

To form the final URL ID we prepend three random characters. This makes the final ID random and hackers can't just increment it and see all URLs in our database.

It works like this:
1. Counter = 1000
2. Generate base62 number: 
    1. 1000 % 62 = 8 <- first digit
    2. 1000/62 = 16
    3. 16 % 62 = 16 <- second digit
    4. final number = `[16, 8]` (reversed)
3. Convert base62 number to string: 16->G, 8->8: `G8`
4. Generate random part: `abc`
5. URL_ID = `abcG8`

Is is then easy to convert URL_ID back to integer:
1. remove first three characters: `abcG8` -> `G8`
2. map characters to integers: [16, 8]
3. calculate 16 * 62^1 + 8 * 62^0 = 16 * 62 + 8 * 1 = 1000

This would be useful if we saved the long URL to a SQL database with an integer primary key. But in our architecture we don't need it.

## Concurrency

I think the app, when deployed to production and provided with the largest Redis instance and a lot of API replicas in Kubernetes, can scale to one million concurrent users. However the main bottleneck for this would then be Python itself.

### Architectural solution

#### Shorten
Because of the base62 algorithm, the only thing needed to generate a new short URL is to perform an `INCR` operation in Redis. Since Redis is atomic and can support hundreds of thousands requests per second, there is no bottleneck. 

#### Redirect
When the short URL is requested for the first time, it's saved to Redis (with expiration time 24 hours). So if URL is popular, it's in Redis all the time, S3 bucket is not accessed and everything is fast. 

There is a risk that Redis would fill up - in that case a more elaborate Redis structure (e.g. ordered set) could be used to rank the URLs by popularity and periodically remove the least popular ones.

### Technical solution

I tried to use `async` where possible:

* `API`: `FastAPI` has natively `async`
* `Redis`: `aioredis` package, use of `await` when communicating with Redis
* `S3`: `boto3` package with needed methods decorated to be async

I use `uvicorn` web server - for production is recommended `gunicorn` (prepared in `docker-compose.yaml`). We can set number of workers via `WEB_CONCURRENCY` env (it's not valid with reload option for local development). 

### Load testing

#### Setup

Edit `docker-compose.yaml`:
* uncomment env `LOAD_TEST=1`: disable logging
* comment env `DEBUG=1`: for FastAPI
* command: uncomment `--no-access-log` for `uvicorn`

We used [Locust](https://locust.io/) library to load test the app. 

1. `pip3 install locust`
2. `locust`

#### Results

* 100 concurrent users for `/redirect` endpoint: 600 rps, 150ms median response time
* 1000 concurrent users for `/redirect` endpoint: 500 rps, 1500ms median response time

The results for 1000 users are not very good - there is probably a bottleneck, but I'm not sure where.

Tests were run on Macbook Pro 13" - not a very powerful machine. Also Locust was run on the same machine and could drain some resources.

And for the record, Uvicorn server was better than gunicorn.

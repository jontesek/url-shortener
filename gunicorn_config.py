"""Link to docs: http://docs.gunicorn.org/en/stable/settings.html."""

timeout = 60
graceful_timeout = 60  # to sync with terminationGracePeriodSeconds in K8S
keepalive = 65  # to prevent a race condition between the GCP Load Balancer and gunicorn default keepalive timeout
worker_class = "gevent"
max_requests = 100000
max_requests_jitter = 2000

preload_app = True
bind = ":8080"

loglevel = "info"
# accesslog = "-"  # send access log to stdout

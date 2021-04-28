import structlog

from .settings import local

if not local:
    structlog.configure(processors=[structlog.processors.JSONRenderer()])

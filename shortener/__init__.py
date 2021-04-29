import logging

import structlog

from .settings import LOAD_TEST, local

if not local:
    structlog.configure(processors=[structlog.processors.JSONRenderer()])

if LOAD_TEST:
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING),
    )

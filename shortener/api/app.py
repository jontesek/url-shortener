import ddtrace
import sentry_sdk
from ddtrace_asgi.middleware import TraceMiddleware
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration

from .. import settings
from .routers.health import router as health_router
from .routers.redirect import router as redirect_router
from .routers.shorten import router as shorten_router


def create_app():
    # pylint: disable=redefined-outer-name
    app = FastAPI(
        title="Shortener",
        description="Concurrent URL shortener",
        version="0.1.0",
        debug=settings.DEBUG,
    )

    if not settings.local:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            integrations=[LoggingIntegration(level=None, event_level=None)],
        )
        app.add_middleware(SentryAsgiMiddleware)

        ddtrace.tracer.configure(
            hostname=str(settings.DD_HOSTNAME), port=int(settings.DD_TRACER_PORT)
        )
        app.add_middleware(
            TraceMiddleware,
            service=settings.APP_NAME,
            tags={"env": settings.ENVIRONMENT},
        )

    app.include_router(health_router)
    app.include_router(shorten_router)
    app.include_router(redirect_router)

    return app


app = create_app()

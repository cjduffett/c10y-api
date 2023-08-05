"""Application and routes."""

from starlette.applications import Starlette
from starlette.routing import Route

from . import db, endpoints


def create_app() -> Starlette:
    """Initialize application and database."""
    
    db.create_tables()

    # Bind endpoints to application routes
    all_routes = [
        # TODO: API versioning, e.g. /api/v1/...
        Route("/health", endpoints.Health),
    ]

    # Create the application
    c10y_app = Starlette(routes=all_routes)
    return c10y_app


# Application object that the uvicorn ASGI will serve
c10y_app = create_app()

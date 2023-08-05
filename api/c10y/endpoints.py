"""Constituency API endpoints."""

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import PlainTextResponse


class Health(HTTPEndpoint):
    """Health check endpoint."""

    async def get(self, request: Request):
        """Check server health/readiness."""

        return PlainTextResponse("OK")

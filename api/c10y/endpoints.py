"""Constituency API endpoints."""

import jinja2
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse, HTMLResponse

from . import services


class Health(HTTPEndpoint):
    """Health check endpoint."""

    async def get(self, request: Request):
        """Check server health/readiness."""

        return PlainTextResponse("OK")


class Index(HTTPEndpoint):
    """Index view that displays a list of constituents."""

    async def get(self, request: Request):
        """Load main index.html page."""

        jinja_env = _jinja_env()
        template = jinja_env.get_template("index.html")

        constituents = services.list_constituents()

        return HTMLResponse(template.render(constituents=constituents))


class ConstituentList(HTTPEndpoint):
    """Constituent list endpoint."""

    async def get(self, request: Request):
        """List all constituents in the database, sorted alphabetically."""

        # TODO: Pagination, limit result set we return at any given time to what can be
        # reasonably displayed in a list on the page.
        constituent_list = services.list_constituents()

        # Format as JSON. TODO: Define request/response schemas, ideally compatible
        # with OpenAPI spec. See: https://www.starlette.io/schemas/
        response_json = {
            "count": len(constituent_list),
            "constituents": [
                {   
                    # We probably don't need _every_ field in the list view, just some primary ones
                    "first_name": c.first_name,
                    "last_name": c.last_name,
                    "email": c.email,
                    "city": c.city,
                    "state": c.state,
                }
                for c in constituent_list
            ]
        }

        return JSONResponse(response_json)


def _jinja_env() -> jinja2.Environment:
    """Configure Jinja2 HTML template engine."""

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader("www", encoding="utf-8"),
        autoescape=jinja2.select_autoescape(),
    )

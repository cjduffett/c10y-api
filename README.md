# Constituency API

Elected official's constituency (c10y) data API.

## Dependencies

* Install [Docker](https://docs.docker.com/get-docker/)
* Install [`make`](https://www.gnu.org/software/make/manual/make.html)

## Quick Start

Build the project:
```
make build
```

Run the app:
```
make run
```

Get a shell:
```
make shell
```

## Endpoints

Application is available at http://localhost:8000

### Health Check

Request:
```
GET /health
```

Response: `200 OK`
```
OK
```

## Resources

* [Poetry](https://python-poetry.org) - Python dependency management
* [Starlette](https://www.starlette.io) - Fast async Python web framework
* [Sqlalchemy](https://docs.sqlalchemy.org/en/20/) - Python database ORM

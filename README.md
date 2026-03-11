<div align="center">
    <img
        src="https://github.com/jcbianic/flask-jeroboam/blob/main/docs/_static/img/jeroboam_logo_with_text.png"
        width="400px"
        alt="jeroboam-logo">
    </img>
</div>

<h1 align="center">Flask-Jeroboam</h1>

<p align="center">
    <a href="README.md">English</a> | <a href="README_fr.md">Français</a>
</p>

<div align="center">

<i>Use FastAPI's elegant parameter syntax in your Flask applications.</i>

[![PyPI](https://img.shields.io/pypi/v/flask-jeroboam.svg)][pypi_]
[![Python Version](https://img.shields.io/pypi/pyversions/flask-jeroboam)][python version]
[![Download](https://img.shields.io/pypi/dm/flask-jeroboam)][downloads]
[![License](https://img.shields.io/github/license/jcbianic/flask-jeroboam?color=green)][license]
[![Commit](https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam?color=green)][commit]

[![Read the documentation at https://flask-jeroboam.readthedocs.io/](https://img.shields.io/readthedocs/flask-jeroboam/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Coverage](https://codecov.io/gh/jcbianic/flask-jeroboam/graph/badge.svg)][codecov]
[![Tests](https://github.com/jcbianic/flask-jeroboam/workflows/Tests/badge.svg)][tests]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)][ruff]

[pypi_]: https://pypi.org/project/flask-jeroboam/
[status]: https://pypi.org/project/flask-jeroboam/
[downloads]: https://img.shields.io/pypi/dm/flask-jeroboam
[python version]: https://pypi.org/project/flask-jeroboam
[read the docs]: https://flask-jeroboam.readthedocs.io/
[tests]: https://github.com/jcbianic/flask-jeroboam/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/jcbianic/flask-jeroboam
[pre-commit]: https://github.com/pre-commit/pre-commit
[ruff]: https://github.com/astral-sh/ruff
[commit]: https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam

</div>

---

**Documentation**: [https://flask-jeroboam.readthedocs.io/](https://flask-jeroboam.readthedocs.io/)

**Source Code**: [https://github.com/jcbianic/flask-jeroboam](https://github.com/jcbianic/flask-jeroboam)

---

## What is Flask-Jeroboam?

Flask-Jeroboam brings FastAPI's approach to Flask. If you like how FastAPI handles request parsing, response validation, and automatic docs—but you need Flask instead—this is for you.

It inspects your endpoint function signatures and handles validation, serialization, and OpenAPI docs automatically. It's just a thin layer connecting Flask to Pydantic the way FastAPI does.

## Why Flask-Jeroboam?

**You have existing Flask code** — Refactoring to FastAPI isn't an option. Jeroboam is a drop-in extension.

**You rely on Flask's ecosystem** — Flask-SQLAlchemy, Flask-Login, Flask-Admin, and dozens of other extensions just work. FastAPI doesn't integrate with them.

**You serve both HTML and APIs** — Some apps need to render templates alongside JSON endpoints. Flask handles both naturally.

**You prefer WSGI** — Whether for infrastructure reasons or team preference, WSGI is your deployment model.

**You want FastAPI's development experience** — Type-safe endpoints with automatic documentation, without switching frameworks.

## Key Features

- **Per-Parameter Validation** — Type hints on endpoint arguments automatically validate and parse request data
- **Response Validation** — Define response models; Jeroboam validates outgoing data matches the schema
- **Automatic OpenAPI Docs** — Interactive API documentation generated automatically
- **Type Safety** — Use Python type hints to make code clearer and catch bugs earlier
- **Drop-In Compatible** — Works with existing Flask applications and extensions

## Quick Install

```console
$ pip install flask-jeroboam
```

Full setup guide with dependency management: [Installation](https://flask-jeroboam.readthedocs.io/en/latest/installation.html)

## A Taste

```python
from flask_jeroboam import Jeroboam, InboundModel, OutboundModel
from typing import Optional

app = Jeroboam(__name__)

class WineQuery(InboundModel):
    page: int = 1
    search: Optional[str] = None

class WineOut(OutboundModel):
    name: str
    appellation: str

@app.get("/wines", response_model=list[WineOut])
def list_wines(query: WineQuery):
    return get_wines(query.page, query.search)
```

Query params are parsed and validated from the type hints. The response is filtered and serialized against `WineOut`. Hit `/docs` for the interactive OpenAPI interface.

## Next Steps

**New to Jeroboam?** Start with the [Getting Started](https://flask-jeroboam.readthedocs.io/en/latest/getting_started.html) guide.

**Ready to build?** Follow the [Tutorial](https://flask-jeroboam.readthedocs.io/en/latest/tutorial/index.html) for a complete example.

**Need specifics?** Check the [How-to Guides](https://flask-jeroboam.readthedocs.io/en/latest/guides/index.html) for common tasks.

**Want deeper understanding?** Read the [Concepts](https://flask-jeroboam.readthedocs.io/en/latest/concepts/index.html) section.

## How Does It Compare?

Flask-Jeroboam sits at a specific point in the landscape—closer to FastAPI than to flask-openapi3 or flask-restx, but firmly in the Flask ecosystem.

| Aspect                | Jeroboam      | flask-openapi3        | FastAPI                 |
| --------------------- | ------------- | --------------------- | ----------------------- |
| Per-parameter hints   | ✅            | ❌ (groups in models) | ✅                      |
| Response validation   | ✅ by default | ⚠️ opt-in             | ✅ by default           |
| Pydantic v2           | ✅            | ✅                    | ✅                      |
| Decorator composition | ✅            | ❌                    | ✅                      |
| Flask compatible      | ✅            | ✅                    | ❌ (separate framework) |
| Async/await           | ❌ (WSGI)     | ❌ (WSGI)             | ✅ (ASGI)               |

See the full [Comparison Guide](https://flask-jeroboam.readthedocs.io/en/latest/alternatives.html) for in-depth analysis.

## About the Name

A Jeroboam is a large wine bottle (5 litres in Bordeaux, 3 litres elsewhere) designed for fine wines that age well. The larger surface-area-to-volume ratio slows oxidation. Temperature stays more stable. They're built to last without degrading your wine.

The project aims for the same durability: an API that stays solid and reliable as it ages.

## License

Distributed under the [MIT License][license]. Flask-Jeroboam is free and open source.

## Issues

Found a bug or want to suggest a feature? Please [file an issue](https://github.com/jcbianic/flask-jeroboam/issues) using the available templates.

## Credits

Inspired by [@tiangolo](https://github.com/tiangolo)'s [FastAPI](https://fastapi.tiangolo.com/).

Built on [Flask](https://flask.palletsprojects.com/) and [Pydantic](https://docs.pydantic.dev/)—both excellent projects.

[license]: https://github.com/jcbianic/flask-jeroboam/blob/main/LICENSE

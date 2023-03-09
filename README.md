<div align="center">
    <img
        src="https://github.com/jcbianic/flask-jeroboam/blob/main/docs/_static/img/jeroboam_logo_with_text.png"
        width="400px"
        alt="jeroboam-logo">
    </img>
</div>
<h1 align="center">Flask-Jeroboam</h1>

<div align="center">

<i>Flask-Jeroboam is a Flask extension modelled after FastAPI. It uses Pydantic to provide easy-to-configure data validation in request parsing and response serialization.</i>

[![PyPI](https://img.shields.io/pypi/v/flask-jeroboam.svg)][pypi_]
[![Python Version](https://img.shields.io/pypi/pyversions/flask-jeroboam)][python version]
[![License](https://img.shields.io/github/license/jcbianic/flask-jeroboam?color=green)][license]
[![Commit](https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam?color=green)][commit]

[![Read the documentation at https://flask-jeroboam.readthedocs.io/](https://img.shields.io/readthedocs/flask-jeroboam/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Maintainability](https://api.codeclimate.com/v1/badges/181b7355cee7b1316893/maintainability)](https://img.shields.io/codeclimate/maintainability/jcbianic/flask-jeroboam?color=green)
[![Test Coverage](https://api.codeclimate.com/v1/badges/181b7355cee7b1316893/test_coverage)](https://img.shields.io/codeclimate/coverage/jcbianic/flask-jeroboam?color=green)
[![Tests](https://github.com/jcbianic/flask-jeroboam/workflows/Tests/badge.svg)][tests]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/flask-jeroboam/
[status]: https://pypi.org/project/flask-jeroboam/
[python version]: https://pypi.org/project/flask-jeroboam
[read the docs]: https://flask-jeroboam.readthedocs.io/
[tests]: https://github.com/jcbianic/flask-jeroboam/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/jcbianic/flask-jeroboam
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[commit]: https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam

</div>

---

**Documentation**: [https://flask-jeroboam.readthedocs.io/](https://flask-jeroboam.readthedocs.io/)

**Source Code**: [https://github.com/jcbianic/flask-jeroboam](https://github.com/jcbianic/flask-jeroboam)

---

Flask-Jeroboam is a thin layer on top of Flask to make request parsing, response serialization and auto-documentation as smooth and easy as in FastAPI.

Its main features are:

- Request parsing based on typed annotations of endpoint arguments
- Response serialization facilitation
- (Planned) OpenAPI auto-Documentation based on the first two

## How to install

You can install _flask-jeroboam_ via [pip] or any other tool wired to [PyPI]:

```console
$ pip install flask-jeroboam
```

## How to use

### A toy example

_Flask-Jeroboam_ subclasses both Flask and Blueprint classes. This means that the **Jeroboam** and **Blueprint** will behave exactly like their Flask counterparts unless you activate their specific behaviours.

```python
from flask_jeroboam import Jeroboam

app = Jeroboam()

@app.get("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run()
```

This toy example would work exactly like a regular Flask app. If you run this file, then hitting the endpoint with `curl localhost:5000/ping` would return the text response `pong`.

Let's try a more significant and relevant example and build a simplified endpoint to retrieve a list of wines. We are wine-themed, after all.

### Searching for wines

Let's consider an endpoint that provides search capability onto a wine repository. It parses and validates three arguments from the query string and feeds them into a CRUD function `get_wines` that return a list of wines as dictionnaries.
Additionally, this endpoint only needs to return the name of the cuvee and the appellation, and discard any other informations. Let's take a look at what it might look like:

```python
from flask_jeroboam import Jeroboam, InboundModel, OutboundModel
from pydantic.fields import Field
from typing import List, Optional
from docs_src.readme.crud import get_wines

app = Jeroboam(__name__)


class GenericPagination(InboundModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class WineOut(OutboundModel):
    cuvee: str
    appellation: str


@app.get("/wines", response_model=List[WineOut])
def read_wine_list(pagination: GenericPagination, search: Optional[str]):
    wines = get_wines(pagination, search)
    return wines


if __name__ == "__main__":
    app.run()
```

Once you've started your server, then hitting the endpoint with `curl "localhost:5000/wines?page=1&perPage=2&search=Champagne"` would return:

```json
[
  {
    "cuvee": "Brut - Blanc de Blancs",
    "appellation": "Champagne"
  },
  {
    "cuvee": "Grande Cuvée - 170ème Edition",
    "appellation": "Champagne"
  }
]
```

All examples in the documentation can be found in `docs_src/X` folder and should run as is. Their corresponding tests can be found in `tests/test_docs/X`.

See the documentation on more advanced usage: [https://flask-jeroboam.readthedocs.io/](https://flask-jeroboam.readthedocs.io/)

## Motivation

I just wanted to use **FastAPI's way** of defining view arguments and response models without leaving Flask.

## A word on performance

One thing **Flask-Jeroboam** won't give you is performance improvement. Underneath Flask, werkzeug still handles the heavy lifting of a wsgi, so transitioning to **Flask-Jeroboam** won't speed up your app. Please remember that FastAPI's performance comes from Starlette, not FastAPI itself.

## Intended audience

The intended audience of **Flask-Jeroboam** is Flask developers who find FastAPI very convincing but also have excellent reasons to stick to Flask.

## About the name of the project

A **Jeroboam** is a large bottle, or flask, containing 5 litres of wine[^1], instead of 0,75. Winemakers use this format for fine wines destined for ageing because it provides better ageing conditions. First, the ratio between the volume of wine it contains and the surface of exchange between the wine and the air is more favourable and slows down the oxidation reaction. These larger containers also take longer to cool down or warm up, leading to less thermal violence to the wine during conservation.

In other words, they are more durable flasks for fine wines. The intention is to hold this promise for APIs.

The wine-themed name is a tribute to the Bordeaux-based wine tech startup where the development of this package started.

[^1]: Outside of the Bordeaux region Jeroboam bottle contain 3 litres, like in Burgundy or Champagne.

## License

Distributed under the terms of the [MIT license][license], **Flask-Jeroboam** is free and open-source software.

## Issues

If you encounter any problems, please [file an issue] following available templates. Templates are available for feature requests, bug reports, documentation updates and implementation betterments.

## Credits

The main inspiration for this project comes from [@tiangolo]'s [FastAPI].
Starting from v0.1.0 it also includes forked code from [FastAPI].
Appropriate credits are added to the module or functions docstrings.

[Flask] and [pydantic] are the two direct dependencies and do most of the work.

I used [@cjolowicz]'s [Hypermodern Python Cookiecutter] template to generate this project.

[@cjolowicz]: https://github.com/cjolowicz
[@tiangolo]: https://github.com/tiangolo
[fastapi]: https://fastapi.tiangolo.com/
[starlette]: https://www.starlette.io/
[flask]: https://flask.palletsprojects.com/
[pydantic]: https://pydantic-docs.helpmanual.io/
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/jcbianic/flask-jeroboam/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/jcbianic/flask-jeroboam/blob/main/LICENSE
[contributor guide]: https://github.com/jcbianic/flask-jeroboam/blob/main/CONTRIBUTING.md
[command-line reference]: https://flask-jeroboam.readthedocs.io/en/latest/usage.html

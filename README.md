<div align="center">
    <img
        src="https://github.com/jcbianic/flask-jeroboam/blob/main/docs/_static/jeroboam_logo_with_text.png"
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

_Flask-Jeroboam_ subclasses both Flask and Blueprint classes. This means that the **Jeroboam** and **APIBlueprint** will behave exactly like their Flask counterparts unless you activate their specific behaviours.

```python
from flask-jeroboam import Jeroboam

app = Jeroboam()

@app.get("ping")
def ping():
    return "pong"
```

This toy example would work exactly like a regular Flask app. You would start your server just like with Flask. `flask run` would do perfectly fine here.

Then hitting the endpoint with `curl localhost:5000/ping` would return the text response `pong`.

Let's try a more significant and relevant example and build a simplified endpoint to retrieve a list of wines. We are wine-themed, after all.

### Searching for wines

Let's consider an endpoint that provides search capability onto a wine repository. It parses and validates three arguments from the query string and feeds them into a CRUD function `get_wines` that return a list of wines and the total count of wines matching the query.
Additionally, this endpoint only needs to return the name of the cuvee and the appellation and discard any other informations. Let's take a look at what it might look like with _Flask-Jeroboam_:

```python
from flask_jeroboam import Jeroboam, Parser, Serializer

app = Jeroboam(__name__)

class PaginatedSearch(Parser):
    page: int = Field(default=1)
    per_page: int = Field(default=10)
    search: Optional[str]

class WineOut(Serializer):
    cuvee: str
    appellation: str

class WineListOut(Serializer):
    wines: WineOut
    count: int
    total_count: int

@app.get("/wines", response_model=WineListOut)
def read_wine_list(wine_search: PaginatedSearch):
    wines, total_count = get_wines(wine_search)
    return {"wines": wines, "count": len(wines), "total_count": total_count}


if __name__ == "__main__":
    app.run()
```

Once you've started your server, then hitting the endpoint with `curl "localhost:5000/wines?page=1&per_page=2&search=Champagne"` would return something like:

```json
{
  "wines": [
    {
      "appellation": "Champagne",
      "cuvee": "Brut - Blanc de Blancs"
    },
    {
      "appellation": "Champagne",
      "cuvee": "Grande Cuvée - 170ème Edition"
    }
  ],
  "count": 2,
  "total_count": 3
}
```

See the documentation on more advanced usage: [https://flask-jeroboam.readthedocs.io/](https://flask-jeroboam.readthedocs.io/)

## Motivation

[FastAPI] has rapidly gained ground in Python Web Development since its inception in late 2018 ([1][survey]). It is indeed a fantastic framework with killer documentation. Besides best-in-class performance, it brings a very compelling API for request parsing and response serialization that speeds up API development and provides an incredibly smooth Developer Experience.

Although trying to reproduce [FastAPI] [Starlette]-based performance in another framework like [Flask] would be rather hard and non-sensical, its API for defining endpoints is fair game. Some excellent Flask extensions deal with request parsing, response serialization, and auto-documentation, but nothing _exactly_ like [FastAPI]. That is what I started exploring with **Flask-Jeroboam**.

[survey]: https://lp.jetbrains.com/python-developers-survey-2021/#FrameworksLibraries
[ref#1]: https://testdriven.io/blog/moving-from-flask-to-fastapi/
[ref#2]: https://developer.vonage.com/blog/21/08/10/the-ultimate-face-off-flask-vs-fastapi
[ref#3]: https://towardsdatascience.com/understanding-flask-vs-fastapi-web-framework-fe12bb58ee75

## A word on performance

One thing **Flask-Jeroboam** won't give you is performance improvement. Underneath Flask, werkzeug still handles the heavy lifting of a wsgi, so transitioning to **Flask-Jeroboam** won't speed up your app. Please remember that FastAPI's performance comes from Starlette, not FastAPI itself.

## Intended audience

The intended audience of **Flask-Jeroboam** is Flask developers who find FastAPI very attractive but also have excellent reasons to stick to Flask.

## About the name of the project

A **Jeroboam** is a large bottle, or flask, containing 3 litres of wine, instead of 0,75 - although outside of the Bordeaux region it can be up to 4,5 litres like in Burgundy or Champagne. Winemakers use this format for fine wines destined for ageing because they provide better conditions. Namely, the ratio between the volume of wine it contains and the surface of exchange between the wine and the air is more favourable and slows down the oxidation reaction. These containers also take longer to cool down or warm up, leading to less thermal violence to the wine during conservation.

In other words, they are more durable flasks for fine wines. The intention is to hold this promise for APIs.

The wine-themed name is a tribute to the Bordeaux-based wine tech startup where the development of this package started.

## License

Distributed under the terms of the [MIT license][license], **Flask-Jeroboam** is free and open-source software.

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

## Credits

The main inspiration for this project comes from [@tiangolo]'s [FastAPI].

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

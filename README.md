<center>

# Flask-Jeroboam

[![PyPI](https://img.shields.io/pypi/v/flask-jeroboam.svg)][pypi_]
[![Python Version](https://img.shields.io/pypi/pyversions/flask-jeroboam)][python version]
[![License](https://img.shields.io/pypi/l/flask-jeroboam)][license]
[![Commit](https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam)][commit]

[![Read the documentation at https://flask-jeroboam.readthedocs.io/](https://img.shields.io/readthedocs/flask-jeroboam/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/jcbianic/flask-jeroboam/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/jcbianic/flask-jeroboam/branch/main/graph/badge.svg)][codecov]
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

</center>

## Motivation

[FastAPI] has been rapidly gaining ground in Python Web Development since its inception in late 2018 ([1][survey]). Besides impressive performance improvement , it brings a very compelling API for request parsing and response serialisation that speed up API development by catering for Developer Experience.

While it is often compared to [Flask], ([1][ref#1], [2][ref#2] and [3][ref#3]), the comparaison feels a bit unfair. FastAPI is, in the words of its creator[@tiangolo] a thin layer on top of [Starlette], a _lightweight ASGI framework/toolkit, ... for building async web services in Python_ and [Pydantic]. To some extend, Flask is more related to Starlette than it is to [FastAPI].

Although there are some excellent Flask extensions dealing with request parsing, response serialisation, and auto-documentation, I wanted something closer to [FastAPI]'s DX. Hence **Flask - Jeroboam**.

[survey]: https://lp.jetbrains.com/python-developers-survey-2021/#FrameworksLibraries
[ref#1]: https://testdriven.io/blog/moving-from-flask-to-fastapi/
[ref#2]: https://developer.vonage.com/blog/21/08/10/the-ultimate-face-off-flask-vs-fastapi
[ref#3]: https://towardsdatascience.com/understanding-flask-vs-fastapi-web-framework-fe12bb58ee75

## Who is it inteded for

For devs who are fond of FastAPI but have perfectly good reasons to stick to Flask, including:

- a large code base build with Flask (although migration could be undertaken)
- being confortable with Flask and not needing the performance of Starlette
- depending on Flask eco-system

## Features

Flask-Jeroboam will provide the following features :

- OpenAPI Auto-Documentation based on endpoint type annotations
- Request parsing with pydantic
- Response serialization facilitation with pydantic

Dependency Injection as featured in FastAPI feels like something you don't need in Flask.

## Installation

You can install _flask-jeroboam_ via [pip], or [poetry] from [PyPI]:

```console
$ pip install flask-jeroboam
```

or better yet with poetry:

```console
$ poetry add flask-jeroboam
```

## Example Usage

Our goal is to implement an API similar, if not equivalent, to the one you have with FastAPI. Because we think it's an excellent standard.

First you would need to replace your existing flask.Blueprint with a flask-jeroboam.ApiBlueprint. Note that APIBlueprint are just regular Blueprint with a extra features, but they should not break any endpoint defined the _flask way_.

```python
from flask-jeroboam import APIBlueprint

router = APIBlueprint("wines", __name__)

@router.get("/wines", response_model=serializers.WineList)
@jwt_required()
def read_example(wines_in: parsers.WineList):
    wines = crud.get_wines(wines_in, db.session)
    return {"items": wines}
```

## License

Distributed under the terms of the [MIT license][license],
**Flask-Jeroboam** is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

The main inspiration of this project comes from [@tiangolo]'s [FastAPI].

The heavy-lifting if performed by [Flask] and [pydantic].

The project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[@tiangolo]: https://github.com/tiangolo
[FastAPI]: https://fastapi.tiangolo.com/
[Starlette]: https://www.starlette.io/
[Flask]: https://flask.palletsprojects.com/
[pydantic]: https://pydantic-docs.helpmanual.io/
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/jcbianic/flask-jeroboam/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/jcbianic/flask-jeroboam/blob/main/LICENSE
[contributor guide]: https://github.com/jcbianic/flask-jeroboam/blob/main/CONTRIBUTING.md
[command-line reference]: https://flask-jeroboam.readthedocs.io/en/latest/usage.html

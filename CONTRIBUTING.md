# Contributor Guide

I appreciate your interest in improving this project. This project is open-source under the [MIT license] and
welcomes contributions in the form of bug reports, feature requests, and pull requests. Currently, our focus is on **improving documentation** and **hunting for bugs**.

We intend to use the [Issue Tracker] to coordinate the community and provide templates for bug reports, feature requests, documentation updates, and implementation improvements. So be sure to use the appropriate template with further instructions on writing any.

## Ressources

Here is a list of important resources for contributors:

- [Source Code]
- [Documentation]
- [Issue Tracker]
- [Code of Conduct]

[mit license]: https://opensource.org/licenses/MIT
[source code]: https://github.com/jcbianic/flask-jeroboam
[documentation]: https://flask-jeroboam.readthedocs.io/
[issue tracker]: https://github.com/jcbianic/flask-jeroboam/issues

## How to set up your development environment

You need Python 3.9+ and the following tools:

- [Poetry]
- [Nox]
- [nox-poetry]

Install the package with development requirements:

```console
$ poetry install
```

You can now run an interactive Python session,
or the command-line interface:

```console
$ poetry run python
$ poetry run flask-jeroboam
```

[poetry]: https://python-poetry.org/
[nox]: https://nox.thea.codes/
[nox-poetry]: https://nox-poetry.readthedocs.io/

## How to test the project

You will need pyenv installed with appropriate python versions available (currently: 3.8 to 3.11) and poetry. Before to run the nox session, you'll need to create a poetry environment for each python version. Unless you do that nox won't have all the python versioned environment to run against and will fail on unavailable verions.

```bash
pyenv local 3.11
poetry env use 3.11
poetry install --with dev

pyenv local 3.10
poetry env use 3.10
poetry install --with dev

pyenv local 3.9
poetry env use 3.9
poetry install --with dev
```

Then you can run all nox sessions:

```bash
nox
```

If you want to run a specific nox session, do:

```bash
nox --session "pre-commit"
```

Run the full test suite:

```console
$ nox
```

List the available Nox sessions:

```console
$ nox --list-sessions
```

You can also run a specific Nox session.
For example, invoke the unit test suite like this:

```console
$ nox --session=tests
```

Unit tests are located in the _tests_ directory,
and are written using the [pytest] testing framework.

[pytest]: https://pytest.readthedocs.io/

## How to submit changes

Open a [pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you can install pre-commit as a Git hook by running the following command:

```console
$ nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

[pull request]: https://github.com/jcbianic/flask-jeroboam/pulls

<!-- github-only -->

[code of conduct]: CODE_OF_CONDUCT.md

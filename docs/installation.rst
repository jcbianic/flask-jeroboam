Installation
============

Install Flask-Jeroboam
----------------------

**Flask-Jeroboam** is published to `PyPI`_, the Python Package Index, and as such, is easily installable using one of the following commands, depending and your tooling for dependency management:

.. tabs::

   .. group-tab:: poetry

      .. code-block:: bash

         $ poetry add flask-jeroboam

   .. group-tab:: pip

      .. code-block:: bash

         $ pip install flask-jeroboam


**Flask-Jeroboam** is now installed along with its two direct dependencies, `Flask`_ and `Pydantic`__ as well as their own dependencies tree. :ref:`see <dependencies>`

If you already have dependency management in Python figured out, skip our next section :ref:`About Dependency Management <about_dep_management>`. If not, :ref:`check it out <about_dep_management>` before moving on to the :doc:`Getting Started Guide </getting_started>` or go to the
:doc:`Documentation Overview </index>`.

.. _Flask: https://palletsprojects.com/p/flask/
.. _Pydantic: https://docs.pydantic.dev/

About Dependency Management
---------------------------

.. _about_dep_management:

Virtual environments
********************

Virtual environments are essential to isolate your project's dependencies from the system-wide packages,
preventing version conflicts and providing reproducibility and ease of deployment to contributors and yourself.
Additionally, it allows for using different versions of packages for various projects on the same machine without conflicts.

It's a good practice, a necessary one even.

I find the combination of `pyenv`_ and `poetry`_ to work very well together, and I will walk you through an example. But anything that's already working for you is fine.

.. _poetry: https://python-poetry.org/
.. _pyenv: https://github.com/pyenv/pyenv
.. _PyPI: https://pypi.org/


Python Version
**************

Your first dependency, and the main one at that, is your Python installation. When you overlook this, you end up using your system default, often outdated, Python installation.

The best practice is to use the latest stable version of Python, which is 3.11 as I write this. :ref:`see how <install-install-python>`. The Python core team is doing an amazing job and it would be a shame to miss out on all the improvement they bring to the game release after release.

That being said, **Flask-Jeroboam** supports Python down to its 3.8 installment. It means that the CI/CD pipeline
tests the package from Python 3.8 to the most recent release. In the future, I will progressively
drop support for older versions but keep up with the newest releases.


Dependencies
************

.. _dependencies:

Installing **Flask-Jeroboam** will automatically install these packages along with their dependencies:

* `Flask`_ obviously: it's the web application framework I'm building this extension upon.
* `Pydantic`_ to provide data validation using Python type annotations.

These two direct dependencies come with their own dependencies tree. In total, you will have up to 9 new packages installed.
There is a nice `poetry`_ command to explore that tree. It goes like this:

::

   $ poetry show flask-jeroboam --tree

   flask-jeroboam 0.0.2a0
   ├── flask >=2.1.3,<3.0.0
   │   ├── click >=8.0
   │   │   └── colorama *
   │   ├── itsdangerous >=2.0
   │   ├── jinja2 >=3.0
   │   │   └── markupsafe >=2.0
   │   └── werkzeug >=2.2.2
   │       └── markupsafe >=2.1.1 (circular dependency aborted here)
   └── pydantic >=1.10.2,<2.0.0
         └── typing-extensions >=4.2.0

.. _Flask: https://palletsprojects.com/p/flask/
.. _Pydantic: https://docs.pydantic.dev/

We that in mind, let's set things up.

A complete installation walkthrough
-----------------------------------

.. note::
   To follow this section, you must have `pyenv`_ and `poetry`_ installed on your system. If this is not the case, follow their respective instructions: `installing pyenv <https://github.com/pyenv/pyenv#installation>`_ and/or `installing poetry <https://python-poetry.org/docs/#installation>`_.


Install the latest Python version
*********************************

.. _install-install-python:

First, you want to pick a specific Python version to install and activate. As said above, the latest stable version is your best option.
Let's install it using `pyenv`_:

.. code-block:: bash

   # Install the latest version of Python
   $ pyenv install 3.11
   # Activate it
   $ pyenv local 3.11
   # Check if it worked
   $ python --version

Once you've secured the correct Python version, you can create a virtual environment for your project.

Create an environment
*********************

.. _install-create-env:

The `poetry`_ CLI can either start the project from scratch (with minimal scaffolding) or hook to an existing project.

In the latter case, the `poetry`_ CLI will prompt you for meta-information like your project's title,
description, author, and license. Don't worry too much about it at this point: you can edit any of this information
in the ```pyproject.toml``` file later on.

Let's assume you're starting a new project without using `poetry`_'s scaffolding capabilities.

.. code-block:: bash

   # Make root dir and move to it
   $ mdir jeroboam-demo && cd jeroboam-demo
   # Create a poetry environment
   $ poetry init
   # Make sure you hooked the env to the intended version of Python
   $ poetry use 3.11

.. _install-activate-env:

Activate the environment
************************

Before you do anything on your project, you must activate the corresponding environment:

.. code-block:: bash

   $ poetry shell

If configured with the right plugins, your shell prompt will change to show the name of the activated environment, which will come handy.

.. note::
   Alternatively, you can use shell plugins to *automatically activates virtual environments created by Poetry* like `zsh-poetry <https://github.com/darvid/zsh-poetry>`.

Add & Install Flask-Jeroboam in your environement
*************************************************

Now you are ready to install **Flask-Jeroboam**. As we've seen before, this would go like this:

.. code-block:: bash

   $ poetry add flask-jeroboam

Testing your installation
**************************

Let's make sure you set up everything correctly. First, create and open a simple file at the root of your project: ``app.py``.

.. code-block:: python
   :caption: app.py
   :linenos:

   from flask-jeroboam import Jeroboam

   app = Jeroboam("JeroboamDemoApp")

   @app.get("/ping")
   def ping():
      return "pong"

   if __name__ == "__main__":
      app.run()

Running this file should start a server on ``localhost:5000``. You can hit that endpoint with a tool like ``curl`` with ``curl http://localhost:5000/ping``
or directly in your browser by going to ``http://localhost:5000/ping``. If either answer with "pong", you did well and are now ready to jump to our :doc:`Getting Started Guide </getting_started>`.

.. note::
   It does not matter how you name your file.

Uninstall Flask-Jeroboam
------------------------

To remove **Flask-Jeroboam** from your project's dependencies is as straightforward as adding it to your project:

.. tabs::

   .. group-tab:: poetry

      .. code-block:: bash

         $ poetry remove flask-jeroboam

   .. group-tab:: pip

      .. code-block:: bash

         $ pip uninstall flask-jeroboam

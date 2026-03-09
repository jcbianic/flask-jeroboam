Setting Things up
=================

If you already have dependency management in Python figured out, skip our next section and jump to the :ref:`walkthrough <walkthrough>`. If not, :ref:`check it out <about_dep_management>` or go to the
:doc:`Documentation Overview </index>`.

.. _Flask: https://palletsprojects.com/p/flask/
.. _Pydantic: https://docs.pydantic.dev/

.. _about_dep_management:

About Dependency Management
---------------------------

Virtual environments
********************

Virtual environments are essential to isolate your project's dependencies from the system-wide packages,
preventing version conflicts and providing reproducibility and ease of deployment to contributors and yourself.
Additionally, it allows for using different versions of packages for various projects on the same machine without conflicts.

It's a good practice, a necessary one even.

`uv`_ handles both Python version management and virtual environments in a single tool, and I will walk you through an example. But anything that's already working for you is fine.

.. _uv: https://docs.astral.sh/uv/
.. _pyenv: https://github.com/pyenv/pyenv
.. _PyPI: https://pypi.org/


Python Version
**************

Your first dependency, and the main one at that, is your Python installation. When you overlook this, you end up using your system's default, often outdated, Python installation.

The best practice is to use the latest stable version of Python, which is 3.13 as I write this. :ref:`see how to install a specific python version <install-install-python>`. The Python core team is doing a fantastic job, and it would be a shame to miss out on all the improvement they bring to the game release after release.

That being said, **Flask-Jeroboam** supports Python 3.10 and above. It means that the CI/CD pipeline
tests the package from Python 3.10 to the most recent release. As python versions reach their end of life, we will drop supporting them but keep up with the newest releases.

.. _walkthrough:

A complete installation walkthrough
-----------------------------------

To follow this section, you must have `uv`_ installed on your system. If this is not the case, follow the `uv installation instructions <https://docs.astral.sh/uv/getting-started/installation/>`_.


Install the latest Python version
*********************************

.. _install-install-python:

First, you want to pick a specific Python version to install and activate. As said above, the latest stable version is your best option.
Let's install it using `uv`_:

.. code-block:: bash

   # Install the latest version of Python
   $ uv python install 3.13
   # Check if it worked
   $ uv run --python 3.13 python --version
   Python 3.13.x

Once you've secured the correct Python version, you can create a virtual environment for your project.

Create an environment
*********************

.. _install-create-env:

`uv`_ can initialise a new project with a ``pyproject.toml`` and a virtual environment in one command:

.. code-block:: bash

   # Create root dir, move to it, and initialise the project
   $ mkdir jeroboam-demo && cd jeroboam-demo
   $ uv init --python 3.13


.. _install-activate-env:

Activate the environment
************************

uv creates and manages the virtual environment for you automatically. You can activate it explicitly if needed:

.. code-block:: bash

   $ source .venv/bin/activate

Or simply prefix commands with ``uv run`` to run them inside the project environment without activating it:

.. code-block:: bash

   $ uv run python

Add & Install Flask-Jeroboam in your environment
*************************************************

Now you are ready to install **Flask-Jeroboam**. As we've seen before, this would go like this:

.. code-block:: bash

   $ uv add flask-jeroboam

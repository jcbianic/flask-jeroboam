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

I find the combination of `pyenv`_ and `poetry`_ to work very well together, and I will walk you through an example. But anything that's already working for you is fine.

.. _poetry: https://python-poetry.org/
.. _pyenv: https://github.com/pyenv/pyenv
.. _PyPI: https://pypi.org/


Python Version
**************

Your first dependency, and the main one at that, is your Python installation. When you overlook this, you end up using your system's default, often outdated, Python installation.

The best practice is to use the latest stable version of Python, which is 3.11 as I write this. :ref:`see how to install a specific python version <install-install-python>`. The Python core team is doing a fantastic job, and it would be a shame to miss out on all the improvement they bring to the game release after release.

That being said, **Flask-Jeroboam** supports Python down to its 3.8 installment. It means that the CI/CD pipeline
tests the package from Python 3.8 to the most recent release. As python versions reach their end of life, we will drop supporting them but keep up with the newest releases.

.. _walkthrough:

A complete installation walkthrough
-----------------------------------

To follow this section, you must have `pyenv`_ and `poetry`_ installed on your system. If this is not the case, follow the following instructions: `installing pyenv <https://github.com/pyenv/pyenv#installation>`_ and `installing poetry <https://python-poetry.org/docs/#installation>`_.


Install the latest Python version
*********************************

.. _install-install-python:

First, you want to pick a specific Python version to install and activate. As said above, the latest stable version is your best option.
Let's install it using `pyenv`_:

.. code-block:: bash

   # Output may vary
   # Install the latest version of Python
   $ pyenv install 3.11
   Downloading Python-3.11.1.tar.xz...
   -> https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tar.xz
   Installing Python-3.11.1...
   Installed Python-3.11.1 to XXXX/.pyenv/versions/3.11.1
   # Activate it
   $ pyenv local 3.11
   # Check if it worked
   $ python --version
   Python 3.11.1

Once you've secured the correct Python version, you can create a virtual environment for your project.

Create an environment
*********************

.. _install-create-env:

The `poetry`_ CLI can either start the project from scratch (with minimal scaffolding) or hook to an existing project.

In the latter case, the `poetry`_ CLI will prompt you for meta information like your project's title,
description, author, and license. Don't worry too much about it now: you can edit any of this information
in the ```pyproject.toml``` file later.

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

If configured with the right plugins, your shell prompt will change to show the name of the activated environment, which will come in handy.

.. note::
   Alternatively, you can use shell plugins to *activate automatically virtual environments created by Poetry* like `zsh-poetry <https://github.com/darvid/zsh-poetry>`_.

Add & Install Flask-Jeroboam in your environment
*************************************************

Now you are ready to install **Flask-Jeroboam**. As we've seen before, this would go like this:

.. code-block:: bash

   $ poetry add flask-jeroboam

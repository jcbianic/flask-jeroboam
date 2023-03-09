Installation
============

Install Flask-Jeroboam
----------------------

I publish **Flask-Jeroboam** to `PyPI`_, the Python Package Index, and as such, it is easily installable using one of the following commands, depending and your tooling for dependency management:

.. tabs::

   .. group-tab:: poetry

      .. code-block:: console

         $ poetry add flask-jeroboam

   .. group-tab:: pip

      .. code-block:: console

         $ pip install flask-jeroboam


With that command, you have installed **Flask-Jeroboam** with its two direct dependencies, `Flask`_ and `Pydantic`_ and their own dependencies tree (:ref:`check it out here <dependencies>`).


.. note::
   We highly recommend installing **Flask-Jeroboam** in a virtual environment. If you need directions on how to do that check out the :doc:`Setting Things Up <tutorial/setting_things_up>` section of our tutorial for more information.

.. _dependencies:

Dependencies
------------

Installing **Flask-Jeroboam** will automatically install these packages along with their dependencies:

* `Flask`_ the web framework heavy lifting is still performed by Flask.
* `Pydantic`_ to provide data validation using Python type annotations.

These two direct dependencies come with their own dependencies tree. In total, you will have up to 9 new packages installed.
There is a nice `poetry`_ command to explore that tree. It goes like this:

.. code-block:: console

   $ poetry show flask-jeroboam --tree
   flask-jeroboam 0.1.0b0 A Flask extension, inspired by FastAPI that uses Pydantic to provide easy-to-configure data validation for request parsing and response serialization.
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

Testing your installation
-------------------------

Let's make sure you set up everything correctly. Create and open a simple file at the root of your project: ``app.py``.

.. literalinclude:: ../docs_src/readme/readme00.py
    :linenos:
    :language: python
    :lines: 2-

Running this file should start a server on ``localhost:5000``. You can hit that endpoint with the command ``curl 'http://localhost:5000/ping'``
or directly in your browser by going to `http://localhost:5000/ping <http://localhost:5000/ping>`_. If either answer with "pong", your installation is functional, and you are ready to jump to our :doc:`Getting Started Guide </getting_started>`.

Uninstall Flask-Jeroboam
------------------------

Removing **Flask-Jeroboam** from your project's dependencies is as straightforward as adding it to your project:

.. tabs::

   .. group-tab:: poetry

      .. code-block:: bash

         $ poetry remove flask-jeroboam

   .. group-tab:: pip

      .. code-block:: bash

         $ pip uninstall flask-jeroboam


.. _poetry: https://python-poetry.org/
.. _pyenv: https://github.com/pyenv/pyenv
.. _PyPI: https://pypi.org/

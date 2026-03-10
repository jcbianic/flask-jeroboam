Installation
============

Install Flask-Jeroboam
----------------------

I publish **Flask-Jeroboam** to `PyPI`_, the Python Package Index, and as such, it is easily installable using one of the following commands, depending and your tooling for dependency management:

.. tabs::

   .. group-tab:: uv

      .. code-block:: console

         $ uv add flask-jeroboam

   .. group-tab:: pip

      .. code-block:: console

         $ pip install flask-jeroboam

   .. group-tab:: poetry

      .. code-block:: console

         $ poetry add flask-jeroboam


With that command, you have installed **Flask-Jeroboam** with its two direct dependencies, `Flask`_ and `Pydantic`_ and their own dependencies tree (:ref:`check it out here <dependencies>`).


.. note::
   We highly recommend installing **Flask-Jeroboam** in a virtual environment. If you need directions on how to do that check out the :doc:`Setting Things Up <tutorial/setting_things_up>` section of our tutorial for more information.

.. _dependencies:

Dependencies
------------

Installing **Flask-Jeroboam** will automatically install these packages along with their dependencies:

* `Flask`_ the web framework heavy lifting is still performed by Flask.
* `Pydantic`_ to provide data validation using Python type annotations.

These two direct dependencies come with their own dependencies tree. In total, you will have around 12 new packages installed.
You can explore that tree with `uv`_:

.. code-block:: console

   $ uv tree --package flask-jeroboam
   flask-jeroboam v0.2.0
   ├── flask v3.1.3
   │   ├── blinker v1.9.0
   │   ├── click v8.3.1
   │   ├── itsdangerous v2.2.0
   │   ├── jinja2 v3.1.6
   │   │   └── markupsafe v3.0.3
   │   └── werkzeug v3.1.6
   │       └── markupsafe v3.0.3 (*)
   ├── pydantic v2.12.5
   │   ├── annotated-types v0.7.0
   │   ├── pydantic-core v2.41.5
   │   │   └── typing-extensions v4.15.0
   │   └── typing-extensions v4.15.0
   └── pydantic-settings v2.13.1
       ├── pydantic v2.12.5 (*)
       └── python-dotenv v1.2.2

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

Troubleshooting
---------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Import Error: No module named 'flask_jeroboam'**

If you encounter this error after installation, ensure:

1. You're using the correct Python environment (activate your virtual environment)
2. The package was installed in the active environment: ``pip list | grep flask-jeroboam``
3. You're using the correct import statement: ``from flask_jeroboam import Jeroboam``

**Version Conflicts**

If you experience version conflicts with Flask or Pydantic:

1. Check your current versions: ``pip show flask pydantic``
2. Ensure Flask >= 3.0 and Pydantic >= 2.0
3. Consider using a fresh virtual environment to isolate dependencies

**Virtual Environment Issues**

If packages aren't being found despite installation:

.. code-block:: console

   $ python -m venv venv
   $ source venv/bin/activate  # On Windows: venv\Scripts\activate
   $ pip install flask-jeroboam

Uninstall Flask-Jeroboam
------------------------

Removing **Flask-Jeroboam** from your project's dependencies is as straightforward as adding it to your project:

.. tabs::

   .. group-tab:: uv

      .. code-block:: bash

         $ uv remove flask-jeroboam

   .. group-tab:: pip

      .. code-block:: bash

         $ pip uninstall flask-jeroboam

   .. group-tab:: poetry

      .. code-block:: bash

         $ poetry remove flask-jeroboam


.. _uv: https://docs.astral.sh/uv/
.. _poetry: https://python-poetry.org/
.. _pyenv: https://github.com/pyenv/pyenv
.. _PyPI: https://pypi.org/

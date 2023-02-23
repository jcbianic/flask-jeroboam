.. rst-class:: hide-header

Welcome
=======

.. image:: _static/jeroboam_logo_with_text.png
    :alt: Flask-Jeroboam: a durable Flask for fine APIs.
    :width: 200px
    :align: center

Welcome to **Flask-Jeroboam**'s documentation.

**Flask-Jeroboam** is a `Flask`_ extension modeled after `FastAPI`_. Like the former, it uses `Pydantic`_
to provide easy-to-configure data validation in request parsing and response serialization, as well as
OpenAPI-compliant documentation auto-generation.

Start with :doc:`installation`, then jump right in with our :doc:`Getting Started Guide </getting_started>`. The
:doc:`Tutorial </tutorial/index>` walks you through a comprehensive example, while the :doc:`API </api>` section gives you details on the components of the extension.

.. note::
   This documentation assumes a certain familiarity with `Flask`_, and `Pydantic`_. If you're new to either, please refer to their respective documentation.
   They are both fantastic.

   - `Flask documentation <https://flask.palletsprojects.com/>`_
   - `Pydantic documentation <https://docs.pydantic.dev/>`_

.. _Flask: https://www.palletsprojects.com/p/flask/
.. _Pydantic: https://docs.pydantic.dev/
.. _FastAPI: https://fastapi.tiangolo.com/

User's Guide
------------

This guide will walk you through how to use Flask-Jeroboam.

.. toctree::
   :maxdepth: 2

   installation
   getting_started
   how_to/index
   tutorial/index

API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Additional Notes
----------------

.. toctree::
   :maxdepth: 2

   contributing
   codeofconduct
   license
   changes

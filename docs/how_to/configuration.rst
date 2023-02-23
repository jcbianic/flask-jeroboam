Configuration
=============

Configuration options let you:

- Opt out of high-level features (e.g. OpenAPI AutoDocumentation)
- Handle OpeanAPI MetaData (e.g. API title, version, description, etc.)

They are prefixed with ``JEROBOAM_`` to avoid name collisions with other packages.


Content
~~~~~~~

- `General Options`_

  * `JEROBOAM_REGISTER_OPENAPI`_
  * `JEROBOAM_REGISTER_ERROR_HANDLERS`_

- `OpenAPI MetaData`_

  * `JEROBOAM_TITLE`_
  * `JEROBOAM_VERSION`_
  * `JEROBOAM_DESCRIPTION`_
  * `JEROBOAM_TERMS_OF_SERVICE`_
  * `JEROBOAM_CONTACT`_
  * `JEROBOAM_LICENCE_INFO`_
  * `JEROBOAM_OPENAPI_VERSION`_
  * `JEROBOAM_SERVERS`_
  * `JEROBOAM_OPENAPI_URL`_

General Options
~~~~~~~~~~~~~~~

General Options let you opt out of some of the **Flask-Jeroboam**'s features, in case you don't need them, need to customize, or if they are interfering with the rest of your app.

.. _JEROBOAM_REGISTER_OPENAPI:
.. py:data:: JEROBOAM_REGISTER_OPENAPI

    It controls whether the OpenAPI Blueprint will be registered when you call the ``init_app`` method on the app instance.

    Set to ``False`` if you don't want the OpenAPI Blueprint to be registered or if you want to plug in your own view functions to serve OpenAPI functionnalities.

    Default: ``True``


.. _JEROBOAM_REGISTER_ERROR_HANDLERS:
.. py:data:: JEROBOAM_REGISTER_ERROR_HANDLERS

    It controls whether package-defined error handlers of **Flask-Jeroboam**'s Exceptions will be registered when you call the ``init_app`` method on the app instance.

    Set to ``False`` if you don't want the package-defined error handlers registered. Note that if you do this, you will need to define your own error handlers for the following exception: ``RessourceNotFound``, ``InvalidRequest`` and ``ResponseValidationError``.

    Default: ``True``


OpenAPI MetaData
~~~~~~~~~~~~~~~~

OpenAPI MetaData Configuration options let you control the MetaData of your OpenAPI Documentation, like its title, versions, contact information, etc... Setting these is optional, meaning you will have an OpenAPI page up and running before setting these options.

.. _JEROBOAM_TITLE:
.. py:data:: JEROBOAM_TITLE

    The title of your API. It will appear as the main title of your OpenAPI documentation page.

    Default: ``app.name``


.. _JEROBOAM_VERSION:
.. py:data:: JEROBOAM_VERSION

    The version of your API. Not to be mistaken with the OPENAPI version. It will appear in the small grey tag next to your title.

    Default: ``0.1.0``


.. _JEROBOAM_DESCRIPTION:
.. py:data:: JEROBOAM_DESCRIPTION

    A short description of your API. It will appear in the small grey tag next to your title.

    Default: ``None``


.. _JEROBOAM_TERMS_OF_SERVICE:
.. py:data:: JEROBOAM_TERMS_OF_SERVICE

        A link to the terms of service of your API. It will appear in the footer of your OpenAPI documentation page.

        Default: ``None``

.. _JEROBOAM_CONTACT:
.. py:data:: JEROBOAM_CONTACT

    A dictionary containing the contact information of your API. It will appear in the footer of your OpenAPI documentation page.

    Default: ``None``

.. _JEROBOAM_LICENCE_INFO:
.. py:data:: JEROBOAM_LICENCE_INFO

    A dictionary containing the licence information of your API. It will appear in the footer of your OpenAPI documentation page.

    Default: ``None``


.. _JEROBOAM_OPENAPI_VERSION:
.. py:data:: JEROBOAM_OPENAPI_VERSION

    The version of the OpenAPI specification that your API is compliant with. It will appear in the footer of your OpenAPI documentation page.

    Default: ``3.0.2``


.. _JEROBOAM_SERVERS:
.. py:data:: JEROBOAM_SERVERS

    A list of dictionaries containing the servers that your API is available on. It will appear in the footer of your OpenAPI documentation page.

    Default: ``[]``


.. _JEROBOAM_OPENAPI_URL:
.. py:data:: JEROBOAM_OPENAPI_URL

    The URL of your OpenAPI documentation page.

    Default: ``/docs``

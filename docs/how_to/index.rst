How-To Guides
=============

In this part of the documentation, we will cover various aspects of **Flask-Jeroboam** features in-depth.

.. toctree::
    :caption: Contents:
    :maxdepth: 2

    view_arguments
    response_serialization
    openapi_autodocumentation
    configuration


Inbound Data Parsing and Validation with View Arguments
-------------------------------------------------------

View arguments are an easy and powerful way to define the parsing, validation and injection of inbound data of your views functions. **Flask-Jeroboam** uses type hints, default values on arguments and sensible inference to make it as concise as possible for you to define this inbound interface of your endpoints. It leverages Pydantic_ to do the heavy lifting of parsing and validating the data.

Learn :doc:`how </how_to/view_arguments>` and make your endpoints more robust and concise.

.. _Pydantic: https://pydantic-docs.helpmanual.io/

Response Serialization with ``response_model``
----------------------------------------------

API endpoints have two interfaces. View Arguments is how you define their inbound interface. Adding a ``response_model`` is how you define their outbound interface. It will then be able to serialize the data returned by your view function to the format you want.

Learn :doc:`how </how_to/response_serialization>` and make your endpoints more robust and concise.


OpenAPI AutoDocumentation
-------------------------

Although defining the inbound and outbound interfaces primary purpose is to provide run-time parsing, validation and de/serialization of inbound and outbound data for your endpoint, they also offer a great opportunity to generate automatically a `OpenAPI <https://swagger.io/specification/>`_ documentation for your API.

Also most of it will happen without you having to write a single line of code. Learn :doc:`how </how_to/openapi_autodocumentation>` you can improve your documentation.


Configuration
-------------

Configuration options let you:

- `Opt out <configuration.html#general-options>`_ of high-level features (e.g. OpenAPI AutoDocumentation)
- Handle `OpeanAPI MetaData <configuration.html#opeanapi-metadata>`_  (e.g. API title, version, description, etc.)

They are prefixed with ``JEROBOAM_`` to avoid name collisions with other packages.

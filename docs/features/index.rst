In-Depth Features Tour
======================

In this part of the documentation, we will cover **Flask-Jeroboam**'s features in-depth to give you a solid understanding of how the package works and how to best use it.

**Flask-Jeroboam**'s purpose is to let you focus on your web app business logic by providing a way to easily define your endpoints inbound and outbound interfaces. The inbound interface defines how clients can interact with your endpoints, while the outbound interface defines what clients can expect from them.


Defining endpoints' inbound interface with view function arguments
------------------------------------------------------------------

You define the parsing, validation, and injection of inbound data into your views functions simply through their arguments, using a combination of type hints, default values, and sensible implicit values to make it as concise as possible.

Learn :doc:`how to define your endpoints' inbound interface </features/inbound>` to make them more concise and robust.

.. toctree::
    :maxdepth: 2

    inbound

.. _Pydantic: https://pydantic-docs.helpmanual.io/

Defining endpoints' outbound interface with route decorators
------------------------------------------------------------

You define your endpoints' outbound interface through the route decorators, typically by passing a ``response_model`` to the decorator. **Flask-Jeroboam** will use it to validate and serialize your view function's returned value.

Learn :doc:`how to define your endpoints' outbound interface </features/outbound>` and be confident that the data you send back follows the schema you choose for them.


.. toctree::
    :maxdepth: 2

    outbound


OpenAPI AutoDocumentation
-------------------------

While defining the inbound and outbound interfaces' primary purpose is to provide run-time parsing, validation, and de/serialization of inbound and outbound data for your endpoint, they also offer an excellent opportunity to generate an `OpenAPI <https://swagger.io/specification/>`_ documentation automatically for your API.

Although most of it will happen without you having to write a single line of code, learn :doc:`how </features/openapi>` you can improve your documentation.


.. toctree::
    :maxdepth: 2

    openapi


Configuration
-------------

Configuration options let you:

- `Opt out <configuration.html#general-options>`_ of high-level features (e.g. OpenAPI AutoDocumentation)
- Handle `OpeanAPI MetaData <configuration.html#opeanapi-metadata>`_  (e.g. API title, version, description, etc.)

We prefixed them with ``JEROBOAM_`` to avoid name collisions with other packages.

.. toctree::
    :maxdepth: 2

    configuration

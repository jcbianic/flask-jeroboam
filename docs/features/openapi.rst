OpenAPI's Auto-Documentation
============================

In addition to providing request-handling functionalities, defining inbound and outbound interfaces lets you benefit from auto-generated documentation with little extra effort. It is as easy as calling the ``init_app`` method on your Jeroboam app instance. This will register an internal blueprint with two endpoints. One serves the OpenaAPI documentation in JSON format, and another serves the Swagger UI.

.. literalinclude:: /../docs_src/features/openapi.py
  :linenos:
  :language: python
  :lines: 2-


You can check it out at `<localhost:5000/openapi>`_ and `<localhost:5000/docs>`_.

Turning it off
--------------

If you don't want to use the auto-documentation feature, turn it off by setting the configuration  ``JEROBOAM_REGISTER_OPENAPI`` flag to ``False``.

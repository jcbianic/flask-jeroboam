How to configure Flask-Jeroboam
===============================

Flask-Jeroboam works out of the box, but you can customize its behavior to match your needs.

Disabling OpenAPI docs
----------------------

If you don't want Jeroboam to generate API documentation:

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["JEROBOAM_REGISTER_OPENAPI"] = False

The ``/docs`` and ``/openapi.json`` endpoints won't be registered.

Customizing the docs URL
------------------------

Change where the documentation is served:

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["JEROBOAM_OPENAPI_URL"] = "/api-docs"

Now access docs at ``/api-docs`` instead of ``/docs``.

Changing the OpenAPI title
---------------------------

Customize the API title in documentation:

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["JEROBOAM_TITLE"] = "Wine Catalog API"
    app.config["JEROBOAM_DESCRIPTION"] = "Manage wines in our catalog"
    app.config["JEROBOAM_VERSION"] = "1.0.0"

These appear in the OpenAPI schema and documentation UI.

Disabling automatic error handlers
----------------------------------

Jeroboam registers generic error handlers for validation errors. To disable:

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["JEROBOAM_REGISTER_ERROR_HANDLERS"] = False

You'll need to handle validation errors yourself.

Response validation
-------------------

Response validation is always active when a ``response_model`` is specified. You can disable it per-endpoint:

.. code-block:: python

    @app.get("/items", response_model=ItemOut, validate_response=False)
    def list_items():
        return fetch_items()

There is no global switch to disable response validation. Control it on each endpoint where needed.

Using with application factory pattern
--------------------------------------

If you use Flask's application factory pattern:

.. code-block:: python

    from flask_jeroboam import Jeroboam

    def create_app(config_name="development"):
        app = Jeroboam(__name__)
        app.config.from_object(f"config.{config_name}")

        # Your blueprints here

        app.init_app()
        return app

Call ``init_app()`` after registering your views to register error handlers and OpenAPI endpoints.

Configuration with environment variables
----------------------------------------

Load configuration from the environment:

.. code-block:: python

    import os
    from flask_jeroboam import Jeroboam

    app = Jeroboam(__name__)
    app.config["JEROBOAM_TITLE"] = os.getenv("API_TITLE", "My API")
    app.config["JEROBOAM_REGISTER_OPENAPI"] = os.getenv("OPENAPI_ENABLED", "true").lower() == "true"

Then set environment variables when running:

.. code-block:: bash

    API_TITLE="Production API" OPENAPI_ENABLED=false python app.py

Custom error responses
----------------------

Customize how validation errors are formatted:

.. code-block:: python

    from flask_jeroboam import Jeroboam
    from flask import jsonify

    app = Jeroboam(__name__)

    @app.errorhandler(422)
    def handle_validation_error(e):
        # Custom format for validation errors
        return jsonify({"errors": e.description}), 422

Validation errors now return your custom format.

Response headers
----------------

Add headers to all responses or specific endpoints:

.. code-block:: python

    @app.after_request
    def add_headers(response):
        response.headers["X-API-Version"] = "1.0.0"
        return response

    @app.get("/items")
    def list_items():
        return fetch_items()

All responses include the custom header.

Caching responses
-----------------

Cache responses to improve performance:

.. code-block:: python

    from flask_caching import Cache

    app = Jeroboam(__name__)
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    @app.get("/items")
    @cache.cached(timeout=3600)
    def list_items():
        return fetch_all_items()

This caches the response for 1 hour. Combining Jeroboam with Flask extensions like Flask-Caching works seamlessly.

CORS configuration
------------------

Enable CORS if your API is accessed from a browser:

.. code-block:: python

    from flask_cors import CORS
    from flask_jeroboam import Jeroboam

    app = Jeroboam(__name__)
    CORS(app)

    @app.get("/items")
    def list_items():
        return fetch_items()

Jeroboam works with standard Flask extensions without issues.

Logging and debugging
---------------------

Enable Flask's debug mode to see full error traces:

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["DEBUG"] = True
    app.run()

In debug mode, validation errors include stack traces and details. Disable in production.

Performance tuning
------------------

For high-traffic APIs, consider these optimizations:

.. code-block:: python

    app = Jeroboam(__name__)

    # Disable verbose logging
    app.logger.setLevel("WARNING")

    # Use a production WSGI server
    app.run()

Remember: use Gunicorn, uWSGI, or similar in production, not ``app.run()``.

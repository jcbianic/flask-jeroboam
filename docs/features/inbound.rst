Inbound interface & view function arguments
===========================================

We will focus here on how to use your view functions arguments to define an endpoint's inbound interface. By inbound interface, we refer to the data a client can send to the server and how.

With **Flask-Jeroboam**, you use a combination of type hints and default values on your view function's arguments to define the inbound interface of your endpoints. This feature enables you to delegate the parsing, validation, and injection of inbound data into your views functions to the extension and focus on your endpoints' business logic.

**Flask-Jeroboam** will handle inbound data based on their location, type and additional validation options. The location refers to how the client passes data over an incoming HTTP request (e.g. query strings, headers, request body...). The type defines the expected shape or schema of the incoming data. Additionally, you can specify extra validation options.

Location
--------

The location concept refers to how the client passes data over an incoming HTTP request. First, we will look into the seven possible locations. Then we will look at the implicit location **Flask-Jeroboam** will assume, and finally at how you can explicitly define the location of every argument of your view functions.


What are locations
~~~~~~~~~~~~~~~~~~

There are various ways to pass data with an HTTP request. Flask and Werkzeug are already parsing the request's raw incoming data to populate members of the ``request`` object accordingly. Defining the location of an argument is a way to tell **Flask-Jeroboam** which ``request``'s member to use to retrieve the incoming data and inject them into your view functions.

There are seven possible locations for view functions arguments.

- Four parameters:

  * ``PATH``: Path parameters are the dynamic parts of an URL found before any ``?`` separator (e.g. ``/items/12``). They are typically used to pass ids. Flask already injects them into your view function.
  * ``QUERY``: Query Strings are equal-sign-separated key-value pairs found in the part of an URL after the ``?`` separator (e.g. ``?page=1``). They serve a variety of purposes. We retrived them from Flask's ``request.args``
  * ``HEADER``: Header parameters are fields destined to pass additional context or metadata about the request to the server. They are colon-separated key-value pair like this ``X-My-Header: 42``. We retrived them ffrom Flask's ``request.headers``
  * ``COOKIE``: Cookies are stored on the client side to keep track of a state in a stateless protocol. They look like this ``Cookie: username=john``, and we retrived them from Flask's ``request.cookies``

- Three variations of the request body:

  * ``BODY``: The request body of an HTTP request is the optional content of the request. Request fetching resources [#3]_ usually don't have one. The request body has a content-type property (like: ``application/json``) that gives the server indication on how to parse them. We retrieve the reuqest body from Flask's ``request.data`` (or ``request.json`` when its mimetype is ``application/json``).
  * ``FORM``: A Request Body with a content-type value of ``application/x-www-form-urlencoded``. We retrieved data from Flask's ``request.form``
  * ``FILE``: Request Body with a enctype of ``multipart/form-data`` and We retrieved data from Flask's ``request.files``

.. [#3] Like ``GET``, ``OPTIONS``, ``HEAD``

Solving Location
~~~~~~~~~~~~~~~~

Most of the time, you won't have to explicitly define your arguments' location, thanks to **Flask-Jeroboam**'s implicit location mechanism. However, you also can explicitly define the location for each argument of your view functions by using special functions on your arguments' default values.

Implicit Location
*****************

We can boiled down **Flask-Jeroboam**'s heuristic to determine the location of an argument to a few simple rules:

- the argument's name will be checked against the the path parameters' names from the endpoint's rule
- arguments of ressource fetching verbs are assumed to be ``QUERY`` parameters
- arguments of ressource creation verbs are assumed to be ``BODY`` parameters

.. warning::
  This is slighly different from **FastAPI**'s heuristic, where singular values are assumed to be ``QUERY`` parameters no matter the verb, and pydantic Models are assumed to be ``BODY`` parameters.

Apart from Path parameters, **Flask-Jeroboam** derives the implicit location of an argument from the HTTP verb of your view function, based on the assumption that for a ``GET`` request, the client typically passes parameters through the query string and that for ``PUT`` and ``POST`` requests the client will mainly use the request body.

Look at the highlighted endpoints below—the first uses ``GET`` (implicit ``QUERY`` location) and the second uses ``POST`` (implicit ``BODY`` location):

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 8,11-21,37-41
  :emphasize-lines: 1,4

You can test them with curl. The highlighted ``GET`` endpoint expects a query string parameter:

.. code-block:: bash

  $ curl 'localhost:5000/implicit_location_is_query_string?page=42'
  Received Page Argument is : 42

while the ``/implicit_location_is_body`` endpoint will expect a page field in the request body.

.. code-block:: bash

  $ curl -X POST 'localhost:5000/implicit_location_is_body' -d '{"page": 42}' -H "Content-Type: application/json"
  Received Page Argument is : 42

Although the two view functions received the same parameter values, notice that we build our request differently by hosting the parameters in two different locations.

In addition to this verb-based mechanism, **Flask-Jeroboam** automatically detects Path parameters. Notice the highlighted route and function below—the ``<int:id>`` in the URL rule and the ``id`` parameter in the function signature match automatically.

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 8,11-16,47-51
  :emphasize-lines: 1,2

Test it:

.. code-block:: bash

  $ curl 'localhost:5000/item/42/implicit'
  Received id Argument is : 42

This also works with other HTTP verbs. Notice the highlighted ``POST`` endpoint below—it has the same path parameter handling despite using a different HTTP verb:

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 8,11-16,52-56
  :emphasize-lines: 8,9

.. code-block:: bash

  $ curl -X POST 'localhost:5000/item/42/implicit'
  Received id Argument is : 42

.. note::
    This implicit location mechanism is one of the reasons why the method decorator (@app.get/put/post VS @app.route) is the preferred way to register a view function in **Flask-Jeroboam**. It enforces the good practice of having a single HTTP verb per view function. View functions assigned to more than one HTTP verb tends to be split up in two mostly independent branches, which depletes their readability.

Although the implicit location will cover most of the cases, you can also define them explicitly.

Explicit Locations
******************

To define explicit locations, you must use one of **Flask-Jeroboam**'s special functions (``Path``, ``Query``, ``Cookie``, ``Header``, ``Body``, ``Form`` or ``File``) to assign default values to your arguments.

Notice the highlighted sections below—the implicit ``GET`` endpoint uses a plain parameter, while the explicit version uses ``Query()``. Both behave identically:

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 8,10,11-16,17-26
  :emphasize-lines: 2,10,15

The same equivalence applies to ``POST`` and ``PUT`` requests. Look at the highlighted examples below—implicit and explicit locations produce the same behavior:

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 6,8,11-16,37-46
  :emphasize-lines: 1,10,15

Test both approaches:

.. code-block:: bash
  :linenos:

  $ curl 'localhost:5000/implicit_location_is_query_string?page=42'
  Received Page Argument is : 42
  $ curl 'localhost:5000/explicit_location_is_query_string?page=42'
  Received Page Argument is : 42
  $ curl -X POST 'localhost:5000/implicit_location_is_body' -d '{"page": 42}' -H "Content-Type: application/json"
  Received Page Argument is : 42
  $ curl -X POST 'localhost:5000/explicit_location_is_body' -d '{"page": 42}' -H "Content-Type: application/json"
  Received Page Argument is : 42

You can also mix implicit and explicit locations. Look at the highlighted code below—the first endpoint uses explicit ``Query()`` and ``Cookie()``, while the second uses implicit locations:

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 7,8,10,11-16,27-36
  :emphasize-lines: 1,11,16

Test both:

.. code-block:: bash
  :linenos:

  $ curl 'localhost:5000/explicit_location_is_query_string_and_cookie?page=42' --cookie "username=john"
  Received Page Argument is : 42. Username is : john
  $ curl 'localhost:5000/implicit_and_explicit?page=42' --cookie "username=john"
  Received Page Argument is : 42. Username is : john

.. note::
  Linters like Flake8 will likely complain about making a function call in an argument default. While this is good advice, it won't cause any unwanted effect in this particular case. You should consider disabling ``B008`` warnings for the files in which you define your view functions.

Assigning default values
************************

As you may have guessed, the special functions are highjacking the default value mechanism to let you easily define an explicit location for your arguments. As a result, their returned value won't be used as a fallback when the client don't provide any argument. In fact, so far, all arguments we have defined are implicitly required because they have no default values to fall back to when the request does not provided them.

Don't take my word for it, let's try it out on the previously defined ``/implicit_location_is_query_string`` endpoint.

.. code-block:: bash

  $ curl -w 'Status Code: %{http_code}\n' 'localhost:5000/implicit_location_is_query_string'
  {"detail":[{"loc":["query","page"],"msg":"field required","type":"value_error.missing"}]}
  Status Code: 400

We received a 400 Bad Request response because we did not provide the required parameter page in our query string. What if we want to set a default value of 1 for the page parameter? There are two ways:

-  With implicit location, define the default value normally in the function signature (e.g., ``page: int = 1``).
-  With explicit location, pass the default value as the first argument to the location function (e.g., ``page: int = Query(1)``).

Look at the highlighted examples below:

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 8,10,11-16,62-71
  :emphasize-lines: 10,15

Test both approaches:

.. code-block:: bash
  :linenos:

  $ curl 'localhost:5000/implicit_location_with_default_value'
  Received Page Argument is : 1
  $ curl 'localhost:5000/implicit_location_with_default_value?page=42'
  Received Page Argument is : 42
  $ curl 'localhost:5000/explicit_location_with_default_value'
  Received Page Argument is : 1
  $ curl 'localhost:5000/explicit_location_with_default_value?page=42'
  Received Page Argument is : 42

The default value is correctly inserted when you don't provide the parameter in the query string for either endpoint. The server returns a valid response, meaning the page parameter is no longer required. Both test cases show that the parsing-validation-injection mechanism is working correctly.

The special functions also provide a way to define additional validation options, but first, let's take a closer look at defining the second part of our inbound arguments: the type.

Type
----

The type refers to the shape or schema of the data you expect. You can assign a type to an argument using type hints. Types can be python built-in types (e.g. ``str``, ``int``, ``float``), pydantic's ``BaseModel`` subclasses or a container of the previous two (e.g. ``List[str]``)

In addition to using type hints, you can also use the first argument of special functions like ``Query``.

Look at the highlighted ``Item`` model definition below:

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 2,3,4,8,10,11-16,72-87
  :emphasize-lines: 3, 12-14

Now see how this model is used. The highlighted function definition below shows different type patterns:

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 2,3,4,8,10,11-16,72-87
  :emphasize-lines: 18

Test it:

.. code-block:: bash

  $ curl 'localhost:5000/defining_type_with_type_hints?page=42&search=foo&search=bar&price=42.42&name=test&count=3'
  Received arguments are :
  page : 42
  search : ['foo', 'bar']
  price : 42.42
  item : name='test' count=3

You'll notice we didn't attempt to pass a dictionary to an ``item`` field to the query string. Instead, we passed two arguments, ``name`` and ``count``, corresponding to the inner fields of Item. Query Strings are usually not a good way to pass nested data structures. If you need to pass a complex data structure, use a different location like a JSON body or a form.

With request bodies, you can choose between embeded or flat arguments.

.. note::
  Type hints are not initially supposed to provide run-time functionality. But this principle was spearheaded by pydantic and later picked up by FastAPI. So we are in good company.

Validation Options
------------------

View function arguments are essentially pydantic model fields, meaning that when you define them, you can leverage every validation feature pydantic offers on model fields.

For number types for instance, you can add ``ge`` (meaning greater or equal to) or ``lt`` (less than) values to define validation conditions on your parameters.

Look at the highlighted example below—notice the ``ge=1`` constraint:

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 8,10,11-16,88
  :emphasize-lines: 4

See what happens when we pass an invalid value (0 is a valid int, but violates the ``ge=1`` constraint):

.. code-block:: bash

  $ curl -w 'Status Code: %{http_code}\n' 'localhost:5000/argument_with_validation?page=0'
  {"detail":[{"ctx":{"limit_value":1},"loc":["query","page"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge"}]}
  Status Code: 400

The server returns a 400 status code with a body giving you direction about the error: it didn't pass the ``ge=1`` validation.

.. note::
  Although you can do it using a special function, I believe that this would lead to bloated view function signatures code in many cases. Beyond a couple of elementary arguments, my preference goes to defining a pydantic BaseModel first with full-blown fields and validation conditions on each of them, and then use that BaseModel as a type hint to define the shape of an inbound argument.

Cheat Sheet
-----------

In summary, your inbound arguments are defined by:

- their location: defined either implicitly or explicitly using special functions as default values (``page:int = Query()``)
- their optional default values: defined either as regular default values ``page:int = 1``or explicitly using special functions (``page:int = Query(1)``)
- their type: using type hint (``page: int``) or the first argument of special functions (``page = Query(int)``)
- their optional validation options: passing additional named arguments to special functions calls (``page:int = Query(ge=1)``)

Next, check out :doc:`how outbound interfaces are defined <outbound>`.

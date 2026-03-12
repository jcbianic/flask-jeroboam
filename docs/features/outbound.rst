Outbound interface & route decorators parameters
================================================

You've seen in the :doc:`previous section </features/inbound>` how to lay out your view functions' argument to define your endpoint's inbound interface. Now we will focus on defining the outbound interface with named arguments to your route decorators.

By outbound interface, we mean the shape of the response your server sends back when hit by the client. It encompasses both the response's :ref:`payload schema <response_model>` and :ref:`status code <status_code>`.

.. _response_model:

Response Model
**************

The response model defines your response payload schema, or in other words, the shape of the data you're sending back to the client. The preferred way to do that is to pass a Pydantic BaseModel to your route decorator's ``response_model`` argument. Alternatively, your view function return value can implicitly define this response model.

.. _add_explicit_response_model:

Explicit Response Model
-----------------------

The most straightforward way of defining the outbound interface of your endpoint is to use the ``response_model`` argument of your route decorator like this ``@app.get("/tasks/<int:task_id>", response_model=Task)``. This argument takes a Pydantic model as a value and will use it to validate and serialize the data returned by your view function.

Let's say you have a ``GET`` endpoint that returns a ``Task``. Look at the highlighted ``Task`` model definition below:

.. literalinclude:: /../docs_src/features/outbound_examples/01_response_model.py
  :linenos:
  :language: python
  :lines: 1-5,11-16
  :emphasize-lines: 1,3,6-10

Now look at the highlighted endpoint that uses this model. The decorator includes ``response_model=Task``, and the function returns only partial data:

.. literalinclude:: /../docs_src/features/outbound_examples/01_response_model.py
  :linenos:
  :language: python
  :lines: 1-5,17-25
  :emphasize-lines: 1,3,7

**Flask-Jeroboam** takes the view function returned value and feeds it into your reponse_model, validates the data, serialize it into JSON, and finally wraps it into a ``Response`` object before handling it back to Flask.

Let's test it out:

.. code-block:: bash

    $ curl http://localhost:5000/tasks/42
    {"id": 42, "name": "Find the answer.", "description": "Just here to make a point."}

As you can see, the endpoint uses the data returned by this view function but also adds the default value of the ``description`` field. This is because **Flask-Jeroboam** uses the ``Task`` model to validate the data returned by the view function. It will add any missing fields and fill them with their default values.

To contrast, look at a simple endpoint without ``response_model``:

.. code-block:: python
  :linenos:

  @app.get("/tasks/<int:task_id>")
  def get_task_simple(task_id: int):
      return {"id": task_id, "title": "Simple task"}

Test it:

.. code-block:: bash

    $ curl http://localhost:5000/tasks/42/no_response_model
    {"id":42,"name":"I'm from the dictionary."}

This time, Flask receive a plain dictionary. It will not add any default value or try to validate it against any schema. It just returns it.

Pydantic's BaseModels are a compelling way to define a complex schema. They are highly reusable and have proven an excellent tool for defining data models. For example, you can nest models, assigning a BaseModel as the type of a parent model field. You can also define validation rules, such as minimum and maximum values, regex patterns... You can even define custom validation rules. For more information on Pydantic models, check out the `Pydantic documentation <https://pydantic-docs.helpmanual.io/>`_.

Alternatively to explicit declarations, you can also let **Flask-Jeroboam** infer the response model from the return values of your view function.

Implicit Response Model
-----------------------

**Flask-Jeroboam** can also derive your response model from the view function return type, but it has to be from annotation. Here’s an example with implicit response model:

.. code-block:: python
  :linenos:

  @app.get("/tasks/<int:task_id>")
  def get_task(task_id: int) -> Task:
      return Task(id=task_id, title="My Task")

Let's test it out.

.. code-block:: bash

    $ curl http://localhost:5000/tasks/42/implicit_from_annotation
    {"id": 42, "name": "Implicit from Annotation", "description": "Just here to make a point."}%
    $ curl -w 'Status Code: %{http_code}\n' http://localhost:5000/tasks/42/implicit_no_annotation
    {"message":"Internal Error"}
    Status Code: 500

However, explicit is better than implicit, so you should prefer the ``response_model`` argument over this approach. Plus, creating the ``Task`` instance feels unnecessarily wordy because, as seen before, you can directly return the dictionary. Speaking of this, let's take a look at allowed return values.

Allowed return values
---------------------

When a response model is defined, **Flask-Jeroboam** can accept the following body from view functions' return values:

- a dictionary
- a dataclass instance
- a list
- a Pydantic model instance
- a Flask response instance (although it will skip the serialization part of its algorithm)

Note that, in addition to the above, you can also return a tuple of the form ``(body, status_code)``, ``(body, headers)``, ``(body, status_code, headers)``. Both the status code and headers will be used in the response. Notably, the :ref:`status_code` will be overridden.

Turning it off
--------------

If you don't want to use **Flask-Jeroboam**'s outbound features, turn it off by setting the ``response_model`` argument to ``None``. It will make **Flask-Jeroboam** ignore the outbound interface of your endpoint.

.. code-block:: python
  :linenos:

  @app.get("/tasks", response_model=None)
  def get_tasks_raw():
      return {"data": [{"id": 1, "title": "Task"}]}

The endpoint still works.

.. code-block:: bash

    $ curl http://localhost:5000/tasks/42/response_model_off
    {"id": 1, "name": "Response Model is off."}

Next, let's look at another aspect of the outbound interface of an endpoint: the successful status code.

.. _status_code:

Status Code
***********

**Flask-Jeroboam** supports both *registration-time* status codes and *return values* status codes.

Registration-time status code
-----------------------------

When you register your view function, **Flask-Jeroboam** will try to solve the status code of the successful response. It will first look at the parameter `status_code` of the route decorator, then at the package-defined default value for the HTTP verb of the route decorator, and finally, the status code attribute of the response class, if any.

.. warning::

    **Flask-Jeroboam** will only be able to use this *registration-time* status code in the OpenAPI documentation of your operation.

We use the following default values for each HTTP verb:

- ``GET``: 200
- ``HEAD``: 200
- ``POST``: 201
- ``PUT``: 201
- ``DELETE``: 204
- ``CONNECT``: 200
- ``OPTIONS``: 200
- ``TRACE``: 200
- ``PATCH``: 200

As you can see, you won't have to set an explicit status code most of the time.

For example, the following endpoint will have a *registration-time* status code of 201. As the view function does not return any status code, a successful put request will give us a 201 status code.

.. code-block:: python

    @app.put("/tasks", response_model=TaskOut)
    def create_task(task: TaskIn):
        return {"task_id": task.id}

.. code-block:: bash

    $ curl -w 'Status Code: %{http_code}\n' -PUT http://localhost:5000/tasks -d '{"name": "My Task"}'
    Status Code: 201
    {"task_id": 1}

Now, let's say we define a second endpoint that takes a task and starts running it. In that case, you might want to override the default (``201``) with a more appropriate ``202`` standing for "Accepted but not done" (see `RFC 7231 <https://tools.ietf.org/html/rfc7231#section-6.3.3>`_). You would do it this way:

.. code-block:: python

    @app.put("/tasks", response_model=TaskOut, status_code=202)
    def create_task(task: TaskIn):
        # Save the Task and Launch it
        return {"task_id": task.id}


This time, when we make a successful request, we will get a ``202`` status code in the response.

.. code-block:: bash

    $ curl -PUT http://localhost:5000/tasks -d '{"name": "My Task"}'
    Status Code: 202
    {"task_id": 1}


Return-value status code
------------------------

**Flask-Jeroboam** also supports returning a status code as a tuple, just like in **Flask**. It will override the *registration-time* status code, but **Flask-Jeroboam** won't be able to adjust the documentation. This could lead to inconsistencies between your documentation and the actual behaviour of the API.

If we revisit the previous example, you could achieve the same *request-handling* result with the following code:

.. code-block:: python

    @app.put("/tasks", response_model=TaskOut)
    def create_task(task: TaskIn):
        # Save the Task and Launch it
        return {"task_id": task.id}, 202


The successful PUT request will still give us a ``202`` status code in the response.

.. code-block:: bash

    $ curl -PUT http://localhost:5000/tasks -d '{"name": "My Task"}'
    Status Code: 202
    {"task_id": 1}

However, the resulting documentation would be different. See :doc:`openapi` for more details.


In summary, when **Flask-Jeroboam** handles the request, it will use the status code inferred at registration time unless the view function returns a value containing a status code.

If you use the OpenAPI documentation, the preferred way is to add a **registration-time** status code to guarantee consistency between your documentation and your API. Also returned status code is also supported to avoid breaking existing code.

Cheatsheet
**********

- To define your responses' payload schema, you pass a pydantic BaseModel to the route decorator named argument ``response_model`` (eg. ``@app.get("/task/<int:id>", response_model=TaskOut)``).
- If you want to override the implicit status code, you can use the named argument ``status_code`` (e.g. ``@app.put("/task/<int:id>/run", status_code=202)``).
- If you want to disable the implicit response model, use the named argument ``response_model=None``. (eg. ``@app.get("/task/<int:id>", response_model=None)``)

Next, check out how to get the most of :doc:`OpenAPI's documentation <openapi>` auto-generation.

.. rubric:: Planned Features

- Templated views (`<https://github.com/jcbianic/flask-jeroboam/issues/105>`_)
- Support Serialization options (e.g. exclude_unset) (`<https://github.com/jcbianic/flask-jeroboam/issues/105>`_)

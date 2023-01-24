Outbound Handler
================

The *Outbound Handler* takes the return value of your view functions, validates it, serializes it, and wraps it into a proper Response instance for the wsgi to send back to the client making the request. It raises an exception when the outbound data isn't valid and produces the OpenAPI documentation describing the response's schemas.

For all these features to work, the Outbound Handler needs a response_model. It has to be a `pydantic.BaseModel` subclass, or a list of such subclasses. The most straightforward way to define a response_model is to use the `response_model` parameter in the route decorator like this:

.. code-block:: python

    from flask-jeroboam import Jeroboam
    from pydantic import BaseModel

    app = Jeroboam()

    class Wine(BaseModel):
        cuvee: str
        appellation: str
        vintage: int

    @app.get("/wines", response_model=List[Wine])
    def read_index_wines():
        return [
            {"cuvee": "Pavillon Rouge", "appellation": "Margaux", "vintage": 2010},
            {"cuvee": "Ropitaux", "appellation": "Meursault", "vintage": 2024}]



Another way to define the response_model is through the return type annotation of the view function you are decorating. Either explicitly:

.. code-block:: python

    @app.get("/wines")
    def read_index_wines() -> List[Wine]:
        return [Wine(**item) for item in [
            {"cuvee": "Pavillon Rouge", "appellation": "Margaux", "vintage": 2010},
            {"cuvee": "Ropitaux", "appellation": "Meursault", "vintage": 2024}]


Or implicitly, although I would discourage the latter because, you know - explicit is better than implicit:

.. code-block:: python

    @app.get("/wines")
    def read_index_wines():
        return [Wine(**item) for item in [
            {"cuvee": "Pavillon Rouge", "appellation": "Margaux", "vintage": 2010},
            {"cuvee": "Ropitaux", "appellation": "Meursault", "vintage": 2024}]


The configured `response_model` (i.e., the one set in the decorator parameters) overwrites the return type annotation. So this is an adequately annotated working example:


.. code-block:: python

    @app.get("/wines", response_model=List[Wine])
    def read_index_wines() -> List[dict]:
        return [
            {"cuvee": "Pavillon Rouge", "appellation": "Margaux", "vintage": 2010},
            {"cuvee": "Ropitaux", "appellation": "Meursault", "vintage": 2024}]


You can also turn off the response_modeling by setting `response_model=None` in the decorator parameters. This will not take into consideration the return type annotation either.


.. code-block:: python

    @app.get("/wines", response_model=None)
    def read_index_wines() -> List[dict]:
        return [
            {"cuvee": "Pavillon Rouge", "appellation": "Margaux", "vintage": 2010},
            {"cuvee": "Ropitaux", "appellation": "Meursault", "vintage": 2024}]


The Outbound Handler will take whatever your view function is returning and try to validate it against its response_model. Now, we have seen thta the response model must be a subclass of a `pydantic.BaseModel` or a list of such subclasses. As for your view functions, they can return anything that a regular flask route can return. Additionally, the body of the response can be an instance of a `pydantic.BaseModel`, `Dict`, A DataClass or a list of the Above. You can also return status_code and headers like in a regular flask route. The Outbound Handler will take care of serializing the response body and wrapping it into a proper Response instance. Here are some examples:

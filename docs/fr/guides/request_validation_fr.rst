Comment valider les données de requête
======================================

Flask-Jeroboam valide automatiquement les requêtes entrantes en fonction de vos signatures de fonction et de vos modèles Pydantic. Ce guide montre des modèles courants pour valider différents types de données de requête.

Paramètres scalaires simples
-----------------------------

Pour les valeurs uniques, utilisez les indices de type directement sur les arguments de la fonction :

.. code-block:: python

    @app.get("/items")
    def get_items(page: int = 1, limit: int = 10):
        # page et limit sont automatiquement validés comme des entiers
        return fetch_items(page, limit)

Essayez de passer des valeurs invalides pour voir les réponses d'erreur automatiques :

.. code-block:: bash

    $ curl "http://localhost:5000/items?page=abc"
    {"detail":[{"loc":["query","page"],"msg":"Input should be a valid integer","type":"int_parsing"}]}

Paramètres de requête vs body
------------------------------

Par défaut, les requêtes GET utilisent des paramètres de requête et les requêtes POST utilisent des paramètres de corps de requête. Si vous devez les mélanger, soyez explicite :

.. code-block:: python

    from flask_jeroboam import Query, Body

    @app.post("/items")
    def create_item(
        # Paramètre de requête (explicite)
        category: str = Query(...),
        # Paramètres du corps (implicite pour POST)
        name: str = Body(...),
        description: str = Body(...)
    ):
        return {"name": name, "description": description, "category": category}

Utiliser des modèles Pydantic
------------------------------

Pour les structures complexes, utilisez des modèles Pydantic. Cela ajoute une validation de schéma :

.. code-block:: python

    from pydantic import BaseModel, Field

    class ItemCreate(BaseModel):
        name: str
        description: str = None
        price: float = Field(..., gt=0)  # Doit être supérieur à 0

    @app.post("/items")
    def create_item(item: ItemCreate):
        # item est validé et fournit l'autocomplétion de l'IDE
        return {"created": item.name}

Contraintes de champ
--------------------

Ajoutez des règles de validation directement dans votre modèle :

.. code-block:: python

    from pydantic import Field, EmailStr

    class UserCreate(BaseModel):
        email: EmailStr  # Automatiquement validé en tant que courrier électronique
        age: int = Field(..., ge=18, le=120)  # Plage 18-120
        username: str = Field(..., min_length=3, max_length=20)
        bio: str = Field("", max_length=500)

Essayez de créer un utilisateur avec des données invalides :

.. code-block:: bash

    $ curl -X POST http://localhost:5000/users \
      -H "Content-Type: application/json" \
      -d '{"email": "not-an-email", "age": 15}'
    {"detail":[{"loc":["body","email"],"msg":"value is not a valid email address"},{"loc":["body","age"],"msg":"Input should be greater than or equal to 18"}]}

Paramètres de chemin
--------------------

Les paramètres de chemin sont détectés automatiquement à partir de la règle d'URL. Aucun travail supplémentaire nécessaire :

.. code-block:: python

    @app.get("/items/<int:item_id>")
    def get_item(item_id: int):
        # item_id est automatiquement validé et injecté
        return fetch_item(item_id)

En-têtes et cookies
-------------------

Validez les en-têtes personnalisés ou les cookies de la même manière :

.. code-block:: python

    from flask_jeroboam import Header, Cookie

    @app.get("/protected")
    def get_protected(
        x_token: str = Header(...),
        session_id: str = Cookie(...)
    ):
        # Les deux sont validés automatiquement
        return {"token": x_token}

Validation conditionnelle
-------------------------

Utilisez les validateurs de Pydantic pour ajouter une logique personnalisée :

.. code-block:: python

    from pydantic import BaseModel, field_validator

    class EventCreate(BaseModel):
        name: str
        start_date: str
        end_date: str

        @field_validator('end_date')
        @classmethod
        def end_after_start(cls, v, info):
            if info.data.get('start_date') and v < info.data.get('start_date'):
                raise ValueError('end_date must be after start_date')
            return v

Cela garantit que end_date est toujours après start_date, même si les deux dates sont individuellement valides.

Champs optionnels
-----------------

Rendez les champs optionnels en utilisant None comme défaut :

.. code-block:: python

    from typing import Optional

    class ItemFilter(BaseModel):
        category: Optional[str] = None
        min_price: Optional[float] = None
        max_price: Optional[float] = None

    @app.get("/items")
    def search_items(filter: ItemFilter):
        # Tous les champs sont optionnels
        return search(filter)

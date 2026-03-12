Comment sérialiser les réponses
===============================

Flask-Jeroboam valide et sérialise vos réponses en utilisant les modèles Pydantic. Cela garantit que votre API retourne les données dans le format attendu et détecte les bugs avant qu'ils n'atteignent les clients.

Modèles de réponse simples
---------------------------

Définissez ce que votre endpoint retourne en utilisant les modèles Pydantic :

.. code-block:: python

    from pydantic import BaseModel

    class ItemOut(BaseModel):
        id: int
        name: str
        price: float

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        item = fetch_item_from_db(item_id)
        return item

Jeroboam valide que votre valeur de retour correspond à ItemOut. Si un champ manque, une erreur est levée en développement.

Listes et collections
---------------------

Retournez des listes en enveloppant le modèle dans un type liste :

.. code-block:: python

    from typing import List

    @app.get("/items", response_model=List[ItemOut])
    def list_items():
        items = fetch_all_items()
        return items

Alias de champ
--------------

Sérialisez avec des noms différents de vos champs Python :

.. code-block:: python

    from pydantic import BaseModel, Field

    class ItemOut(BaseModel):
        id: int
        item_name: str = Field(..., alias="name")
        price_usd: float = Field(..., alias="price")

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        return fetch_item(item_id)

Le JSON de réponse sera ``{"name": "...", "price": ...}`` même si votre code Python utilise des noms différents.

Exclure les champs
------------------

Parfois, vous récupérez plus de données que vous ne voulez les retourner :

.. code-block:: python

    class ItemOut(BaseModel):
        id: int
        name: str
        price: float

        class Config:
            # Seuls ces champs sont inclus dans les réponses
            fields = {"id", "name", "price"}

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        # Le modèle interne peut avoir secret_key, password, etc.
        item = fetch_item_internal(item_id)
        return item  # Seuls id, name, price sont retournés

Réponses imbriquées
-------------------

Utilisez des modèles imbriqués pour les structures complexes :

.. code-block:: python

    from typing import List

    class AuthorOut(BaseModel):
        id: int
        name: str

    class BookOut(BaseModel):
        id: int
        title: str
        author: AuthorOut

    @app.get("/books/<int:book_id>", response_model=BookOut)
    def get_book(book_id: int):
        book = fetch_book_with_author(book_id)
        return book

La réponse inclura l'objet auteur imbriqué, sérialisé automatiquement.

Réponses optionnelles
---------------------

Les endpoints peuvent retourner None parfois :

.. code-block:: python

    from typing import Optional

    @app.get("/items/<int:item_id>", response_model=Optional[ItemOut])
    def get_item_if_exists(item_id: int):
        item = fetch_item(item_id)
        return item  # Pourrait être None

Retourner None sera sérialisé en ``null`` en JSON.

Coercition de type
------------------

Pydantic force les valeurs à correspondre au modèle :

.. code-block:: python

    class ItemOut(BaseModel):
        id: int
        quantity: int

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        # fetch_item retourne les quantités sous forme de chaînes "42"
        item = fetch_item(item_id)
        return item  # Pydantic force "42" à 42

Votre code retourne des chaînes mais la réponse contient des entiers.

Champs calculés
---------------

Ajoutez des champs qui sont calculés à la volée :

.. code-block:: python

    from pydantic import computed_field

    class ItemOut(BaseModel):
        name: str
        quantity: int
        price_each: float

        @computed_field
        @property
        def total_value(self) -> float:
            return self.quantity * self.price_each

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        item = fetch_item(item_id)
        return item

La réponse inclut ``total_value`` même si ce n'est pas dans la base de données. Elle est calculée à partir de quantity et price_each.

Sérialiseurs personnalisés
--------------------------

Transformez les données pendant la sérialisation :

.. code-block:: python

    from datetime import datetime
    from pydantic import BaseModel, field_serializer

    class EventOut(BaseModel):
        name: str
        created_at: datetime

        @field_serializer('created_at')
        def serialize_datetime(self, value: datetime):
            return value.isoformat()

    @app.get("/events/<int:event_id>", response_model=EventOut)
    def get_event(event_id: int):
        event = fetch_event(event_id)
        return event

Les datetimes sont sérialisés en chaînes ISO au lieu du format par défaut.

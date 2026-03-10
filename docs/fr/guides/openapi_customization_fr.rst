Comment personnaliser la documentation de l'API
================================================

Flask-Jeroboam génère la documentation OpenAPI automatiquement, mais vous pouvez la personnaliser selon vos besoins.

Ajouter des descriptions
------------------------

Utilisez les docstrings pour décrire vos endpoints :

.. code-block:: python

    @app.get("/items/<int:item_id>")
    def get_item(item_id: int):
        """
        Récupérer un élément unique par ID.

        Retourne l'élément avec tous ses détails.
        """
        return fetch_item(item_id)

Cette docstring apparaît dans les documents OpenAPI comme la description de l'endpoint.

Documenter les paramètres
--------------------------

Ajoutez des descriptions aux paramètres en utilisant Field :

.. code-block:: python

    from pydantic import Field

    class ItemFilter(BaseModel):
        page: int = Field(1, ge=1, description="Numéro de page, commençant à 1")
        limit: int = Field(10, ge=1, le=100, description="Max d'éléments par page")

    @app.get("/items")
    def list_items(filter: ItemFilter):
        return search_items(filter)

Les paramètres apparaissent maintenant dans les documents avec des descriptions et des règles de validation.

Descriptions de réponse
-----------------------

Documentez ce que votre réponse contient :

.. code-block:: python

    from pydantic import BaseModel

    class ItemOut(BaseModel):
        """Un élément du catalogue."""
        id: int
        name: str = Field(..., description="Le nom d'affichage de l'élément")
        price: float = Field(..., description="Prix en USD")

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        return fetch_item(item_id)

La docstring du modèle et les descriptions des champs apparaissent dans le schéma de réponse.

Personnaliser les endpoints
---------------------------

Utilisez des arguments de décorateur supplémentaires pour personnaliser les métadonnées OpenAPI :

.. code-block:: python

    @app.get(
        "/items",
        summary="Lister tous les éléments",
        tags=["items"]
    )
    def list_items():
        """Obtenez une liste paginée de tous les éléments du catalogue."""
        return fetch_all_items()

Le résumé est court ; la docstring fournit le détail. Les tags organisent les endpoints dans l'interface utilisateur.

Grouper les endpoints avec des tags
-----------------------------------

Utilisez les tags pour organiser les endpoints connexes :

.. code-block:: python

    @app.get("/items", tags=["items"])
    def list_items():
        """Lister les éléments."""
        return fetch_all_items()

    @app.post("/items", tags=["items"])
    def create_item(item: ItemCreate):
        """Créer un nouvel élément."""
        return create_new_item(item)

    @app.get("/orders", tags=["orders"])
    def list_orders():
        """Lister les commandes."""
        return fetch_all_orders()

Dans l'interface Swagger, les endpoints sont groupés sous leurs tags.

Masquer les endpoints des documents
----------------------------------

Certains endpoints pourraient ne pas être publics. Excluez-les :

.. code-block:: python

    @app.get("/internal/health")
    def health_check():
        """Vérifiez si le service fonctionne."""
        return {"status": "ok"}

Les endpoints sont inclus par défaut. Pour en masquer un, utilisez la configuration OpenAPI.

Documenter les erreurs
----------------------

Décrivez quelles erreurs les clients pourraient recevoir :

.. code-block:: python

    from flask_jeroboam import HTTPException

    @app.get("/items/<int:item_id>")
    def get_item(item_id: int):
        """
        Récupérer un élément par ID.

        Lève :
            404 : Élément non trouvé
        """
        item = fetch_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

Documentez vos cas d'erreur pour que les clients sachent à quoi s'attendre.

Authentification dans les documents
-----------------------------------

Marquez les endpoints qui nécessitent une authentification :

.. code-block:: python

    @app.get("/me")
    def get_current_user(authorization: str = Header(...)):
        """
        Obtenez le profil de l'utilisateur actuel.

        Nécessite : Jeton Bearer dans l'en-tête Authorization
        """
        user = verify_token(authorization)
        return user

L'en-tête Authorization apparaît dans les documents comme requis.

Exemples dans les documents
---------------------------

Montrez des requêtes et réponses d'exemple :

.. code-block:: python

    from pydantic import BaseModel

    class ItemOut(BaseModel):
        """Un élément."""
        id: int
        name: str
        price: float

        class Config:
            json_schema_extra = {
                "example": {
                    "id": 1,
                    "name": "Widget",
                    "price": 9.99
                }
            }

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        return fetch_item(item_id)

L'exemple apparaît dans le schéma OpenAPI, visible dans les documents interactifs.

Déprécier les endpoints
-----------------------

Marquez les endpoints qui ne devraient plus être utilisés :

.. code-block:: python

    @app.get("/old-endpoint", deprecated=True)
    def old_endpoint():
        """
        Cet endpoint est obsolète.

        Utilisez /new-endpoint à la place.
        """
        return fetch_data()

Les endpoints dépréciés sont visuellement marqués dans l'interface Swagger.

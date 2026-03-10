Construire votre première API
=============================

Maintenant que vous avez tout configuré, créons une vraie API. Nous allons construire un endpoint de catalogue de vin simple qui montre les trois fonctionnalités principales de Jeroboam : l'analyse des requêtes, la validation des réponses et la documentation automatique.

.. _part-2-fr:

Partie 2 : Votre premier endpoint
**********************************

Commençons par l'endpoint le plus simple possible. Créez un nouveau fichier appelé ``app.py`` :

.. code-block:: python

    from flask_jeroboam import Jeroboam

    app = Jeroboam(__name__)

    @app.get("/wines")
    def list_wines():
        """List all wines in the catalog."""
        return [
            {"name": "Château Lafite", "vintage": 2015},
            {"name": "Château Margaux", "vintage": 2016},
        ]

    if __name__ == "__main__":
        app.run(debug=True)

Lancez-le :

.. code-block:: bash

    $ python app.py

Puis testez-le :

.. code-block:: bash

    $ curl http://localhost:5000/wines
    [{"name":"Château Lafite","vintage":2015},{"name":"Château Margaux","vintage":2016}]

Cela fonctionne exactement comme une application Flask ordinaire. Jeroboam ne fait rien de spécial ici. Juste Flask qui fonctionne comme prévu.

.. _part-3-fr:

Partie 3 : Ajouter la validation des requêtes
**********************************************

Maintenant, ajoutons un paramètre de requête pour filtrer les vins par millésime. Ajoutez ce paramètre à votre fonction :

.. code-block:: python

    @app.get("/wines")
    def list_wines(vintage: int = None):
        """List wines, optionally filtered by vintage."""
        wines = [
            {"name": "Château Lafite", "vintage": 2015},
            {"name": "Château Margaux", "vintage": 2016},
            {"name": "Château Latour", "vintage": 2015},
        ]
        if vintage:
            wines = [w for w in wines if w["vintage"] == vintage]
        return wines

Testez-le :

.. code-block:: bash

    $ curl "http://localhost:5000/wines?vintage=2015"
    [{"name":"Château Lafite","vintage":2015},{"name":"Château Latour","vintage":2015}]

Voilà où Jeroboam commence à faire quelque chose : il a analysé le paramètre de requête et l'a validé comme un entier. Essayez de passer quelque chose qui n'est pas un entier :

.. code-block:: bash

    $ curl "http://localhost:5000/wines?vintage=not_a_number"
    {"detail":[{"loc":["query","vintage"],"msg":"Input should be a valid integer","type":"int_parsing"}]}

Jeroboam a automatiquement validé l'entrée et a retourné une erreur 422 avec le format d'erreur de validation de Pydantic. Vous n'avez écrit aucun code de validation.

Par défaut, les paramètres de fonction non décorés sur les requêtes GET deviennent des paramètres de requête. Pour POST/PUT, ils deviennent des champs de corps de requête. Vous pouvez remplacer cela par des fonctions de paramètres explicites :

.. code-block:: python

    from flask_jeroboam import Query

    @app.get("/wines")
    def list_wines(vintage: int = Query(None)):
        # Same as above—Query() makes it explicit
        ...

.. _part-4-fr:

Partie 4 : Sérialisation des réponses
*****************************

Maintenant, ajoutons un modèle de réponse. Cela valide que tout ce que votre fonction retourne correspond au schéma déclaré :

.. code-block:: python

    from pydantic import BaseModel
    from typing import List

    class WineOut(BaseModel):
        name: str
        vintage: int

    @app.get("/wines", response_model=List[WineOut])
    def list_wines(vintage: int = None):
        """List wines, optionally filtered by vintage."""
        wines = [
            {"name": "Château Lafite", "vintage": 2015},
            {"name": "Château Margaux", "vintage": 2016},
            {"name": "Château Latour", "vintage": 2015},
        ]
        if vintage:
            wines = [w for w in wines if w["vintage"] == vintage]
        return wines

Quand vous appelez l'endpoint maintenant, la réponse est validée et sérialisée à travers le modèle ``WineOut``. Si vous retournez accidentellement un vin manquant un champ, Jeroboam le détecte en développement avant que le client ne le voit.

La validation des réponses est activée par défaut. Elle n'est pas optionnelle. Jeroboam valide toujours les réponses.

.. _part-5-fr:

Partie 5 : Documentation automatique
************************************

Visitez maintenant ``http://localhost:5000/docs`` dans votre navigateur :

.. image:: ../_static/img/GettingStartedOpenAPIDocumentation.png
    :alt: Page de documentation OpenAPI

Vous obtenez une documentation d'API interactive automatiquement. Jeroboam a inspecté votre signature de fonction, vos indices de type et votre modèle de réponse, puis a généré la spec OpenAPI à partir de ceux-ci. Vous n'avez écrit aucun balisage de documentation.

Essayez le bouton "Try it out", entrez un millésime et exécutez la requête. La documentation reflète votre API réelle.

.. _part-6-fr:

Partie 6 : Modèle du monde réel - Pagination
**********************************************

Ajoutons la pagination, un modèle courant du monde réel. Mettez à jour votre fonction :

.. code-block:: python

    from pydantic import Field
    from typing import List

    class WineOut(BaseModel):
        name: str
        vintage: int

    class PaginationParams(BaseModel):
        page: int = Field(1, ge=1)  # ge=1 means >= 1
        per_page: int = Field(10, ge=1, le=100)  # le=100 means <= 100

        @property
        def offset(self) -> int:
            return (self.page - 1) * self.per_page

    @app.get("/wines", response_model=List[WineOut])
    def list_wines(params: PaginationParams, vintage: int = None):
        """List wines with pagination and optional filtering."""
        all_wines = [
            {"name": "Château Lafite", "vintage": 2015},
            {"name": "Château Margaux", "vintage": 2016},
            {"name": "Château Latour", "vintage": 2015},
            {"name": "Château d'Yquem", "vintage": 2010},
            {"name": "Château Pichon", "vintage": 2015},
            {"name": "Château Cos d'Estournel", "vintage": 2016},
        ]

        if vintage:
            all_wines = [w for w in all_wines if w["vintage"] == vintage]

        paginated = all_wines[params.offset : params.offset + params.per_page]
        return paginated

Testez-le :

.. code-block:: bash

    $ curl "http://localhost:5000/wines?page=1&per_page=2"
    [{"name":"Château Lafite","vintage":2015},{"name":"Château Margaux","vintage":2016}]

    $ curl "http://localhost:5000/wines?page=2&per_page=2"
    [{"name":"Château Latour","vintage":2015},{"name":"Château d'Yquem","vintage":2010}]

Essayez de passer une valeur invalide :

.. code-block:: bash

    $ curl "http://localhost:5000/wines?per_page=200"
    {"detail":[{"loc":["query","per_page"],"msg":"Input should be less than or equal to 100","type":"less_than_equal"}]}

Jeroboam valide que ``per_page`` ne dépasse pas 100. Les règles de validation proviennent du modèle Pydantic, et Jeroboam les applique automatiquement.

Visitez à nouveau la documentation à ``http://localhost:5000/docs``. Remarquez que les paramètres page et per_page apparaissent maintenant avec leurs contraintes documentées.

Résumé
**

Vous avez construit une API fonctionnelle avec l'analyse automatique des requêtes, la validation des réponses, une documentation interactive et la pagination avec contraintes.

Rien de cela ne nécessitait d'écrire du code de validation. Jeroboam a extrait les informations de vos indices de type et modèles Pydantic, puis a automatisé le reste.

Prochaines étapes
*

- Lisez :doc:`../guides/index_fr` pour apprendre à gérer des scénarios plus complexes
- Consultez :doc:`../concepts/index_fr` pour comprendre la philosophie de conception
- Explorez le :doc:`../api/index` pour une référence d'API détaillée

Construire votre première API
=============================

Maintenant que vous avez tout configuré, créons une vraie API. Nous allons créer un endpoint simple de catalogue de vin qui met en évidence les trois caractéristiques principales de Jeroboam : l'analyse des requêtes, la validation des réponses et la documentation automatique.

.. _part-2-fr:

Partie 2 : Votre premier endpoint
**********************************

Commençons par l'endpoint le plus simple possible. Créez un nouveau fichier appelé ``app.py`` :

.. code-block:: python

    from flask_jeroboam import Jeroboam

    app = Jeroboam(__name__)

    @app.get("/wines")
    def list_wines():
        """Lister tous les vins du catalogue."""
        return [
            {"name": "Château Lafite", "vintage": 2015},
            {"name": "Château Margaux", "vintage": 2016},
        ]

    if __name__ == "__main__":
        app.run(debug=True)

Lancez-le :

.. code-block:: bash

    $ python app.py

Testez-le ensuite :

.. code-block:: bash

    $ curl http://localhost:5000/wines
    [{"name":"Château Lafite","vintage":2015},{"name":"Château Margaux","vintage":2016}]

Cela fonctionne exactement comme une application Flask ordinaire. Jeroboam ne fait rien de spécial ici. Juste Flask qui fonctionne comme prévu.

.. _part-3-fr:

Partie 3 : Ajouter la validation des requêtes
***********************************************

Maintenant, ajoutons un paramètre de requête pour filtrer les vins par millésime. Ajoutez ce paramètre à votre fonction :

.. code-block:: python

    @app.get("/wines")
    def list_wines(vintage: int = None):
        """Lister les vins, filtrés optionnellement par millésime."""
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

Voici où Jeroboam commence à faire quelque chose : il a analysé le paramètre de requête et l'a validé comme entier. Essayez de passer quelque chose qui n'est pas un entier :

.. code-block:: bash

    $ curl "http://localhost:5000/wines?vintage=not_a_number"
    {"detail":[{"loc":["query","vintage"],"msg":"Input should be a valid integer","type":"int_parsing"}]}

Jeroboam a automatiquement validé l'entrée et renvoyé une erreur 422 au format d'erreur de validation de Pydantic. Vous n'avez écrit aucun code de validation.

Par défaut, les paramètres de fonction non décorés sur les requêtes GET deviennent des paramètres de requête. Pour POST/PUT, ils deviennent des champs du corps de la requête. Vous pouvez remplacer cela par des fonctions de paramètres explicites :

.. code-block:: python

    from flask_jeroboam import Query

    @app.get("/wines")
    def list_wines(vintage: int = Query(None)):
        # Identique à ci-dessus — Query() le rend explicite
        ...

.. _part-4-fr:

Partie 4 : Sérialisation des réponses
***************************************

Maintenant, ajoutons un modèle de réponse. Ceci valide que tout ce que votre fonction retourne correspond au schéma déclaré :

.. code-block:: python

    from pydantic import BaseModel
    from typing import List

    class WineOut(BaseModel):
        name: str
        vintage: int

    @app.get("/wines", response_model=List[WineOut])
    def list_wines(vintage: int = None):
        """Lister les vins, filtrés optionnellement par millésime."""
        wines = [
            {"name": "Château Lafite", "vintage": 2015},
            {"name": "Château Margaux", "vintage": 2016},
            {"name": "Château Latour", "vintage": 2015},
        ]
        if vintage:
            wines = [w for w in wines if w["vintage"] == vintage]
        return wines

Lorsque vous accédez à l'endpoint maintenant, la réponse est validée et sérialisée via le modèle ``WineOut``. Si vous retournez accidentellement un vin sans un champ, Jeroboam le détecte en développement avant que le client ne le voie.

La validation des réponses est activée par défaut. Ce n'est pas optionnel. Jeroboam valide toujours les réponses.

.. _part-5-fr:

Partie 5 : Documentation automatique
*************************************

Visitez maintenant ``http://localhost:5000/docs`` dans votre navigateur :

.. image:: ../../_static/img/GettingStartedOpenAPIDocumentation.png
    :alt: Page de documentation OpenAPI

Vous obtenez une documentation API interactive automatiquement. Jeroboam a inspectionné la signature de votre fonction, les indications de type et le modèle de réponse, puis a généré la spécification OpenAPI à partir de ceux-ci. Vous n'avez écrit aucun balisage de documentation.

Essayez le bouton « Essayer », entrez un millésime et exécutez la requête. Les documents reflètent votre API réelle.

.. _part-6-fr:

Partie 6 : Motif du monde réel - Pagination
*********************************************

Ajoutons la pagination, un motif courant du monde réel. Mettez à jour votre fonction :

.. code-block:: python

    from pydantic import Field
    from typing import List

    class WineOut(BaseModel):
        name: str
        vintage: int

    class PaginationParams(BaseModel):
        page: int = Field(1, ge=1)  # ge=1 signifie >= 1
        per_page: int = Field(10, ge=1, le=100)  # le=100 signifie <= 100

        @property
        def offset(self) -> int:
            return (self.page - 1) * self.per_page

    @app.get("/wines", response_model=List[WineOut])
    def list_wines(params: PaginationParams, vintage: int = None):
        """Lister les vins avec pagination et filtrage optionnel."""
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
******

Vous avez construit une API fonctionnelle avec analyse automatique des requêtes, validation des réponses, documents interactifs et pagination avec contraintes.

Rien de cela n'a nécessité d'écrire du code de validation. Jeroboam a extrait les informations de vos indications de type et de vos modèles Pydantic, puis a automatisé le reste.

Prochaines étapes
*****************

- Lisez :doc:`../guides/index_fr` pour apprendre à gérer des scénarios plus complexes
- Consultez :doc:`../concepts/index_fr` pour comprendre la philosophie de conception
- Explorez la :doc:`../api/index_fr` pour une référence API détaillée

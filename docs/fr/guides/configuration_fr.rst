Comment configurer Flask-Jeroboam
=================================

Flask-Jeroboam fonctionne prêt à l'emploi, mais vous pouvez personnaliser son comportement pour correspondre à vos besoins.

Désactiver la documentation OpenAPI
------------------------------------

Si vous ne voulez pas que Jeroboam génère la documentation d'API :

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["JEROBOAM_REGISTER_OPENAPI"] = False

Les endpoints ``/docs`` et ``/openapi.json`` ne seront pas enregistrés.

Personnaliser l'URL des documents
----------------------------------

Changez où la documentation est servie :

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["JEROBOAM_OPENAPI_URL"] = "/api-docs"

Accédez maintenant aux documents à ``/api-docs`` au lieu de ``/docs``.

Changer le titre OpenAPI
------------------------

Personnalisez le titre de l'API dans la documentation :

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["JEROBOAM_TITLE"] = "Wine Catalog API"
    app.config["JEROBOAM_DESCRIPTION"] = "Manage wines in our catalog"
    app.config["JEROBOAM_VERSION"] = "1.0.0"

Ceux-ci apparaissent dans le schéma OpenAPI et l'interface de documentation.

Désactiver les gestionnaires d'erreurs automatiques
---------------------------------------------------

Jeroboam enregistre les gestionnaires d'erreurs génériques pour les erreurs de validation. Pour désactiver :

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["JEROBOAM_REGISTER_ERROR_HANDLERS"] = False

Vous devrez gérer vous-même les erreurs de validation.

Validation des réponses
-----------------------

La validation des réponses est toujours active quand un ``response_model`` est spécifié. Vous pouvez la désactiver par endpoint :

.. code-block:: python

    @app.get("/items", response_model=ItemOut, validate_response=False)
    def list_items():
        return fetch_items()

Il n'y a pas de commutateur global pour désactiver la validation des réponses. Contrôlez-la sur chaque endpoint selon vos besoins.

Utiliser avec le modèle application factory
-------------------------------------------

Si vous utilisez le modèle application factory de Flask :

.. code-block:: python

    from flask_jeroboam import Jeroboam

    def create_app(config_name="development"):
        app = Jeroboam(__name__)
        app.config.from_object(f"config.{config_name}")

        # Vos blueprints ici

        app.init_app()
        return app

Appelez ``init_app()`` après l'enregistrement de vos vues pour enregistrer les gestionnaires d'erreurs et les endpoints OpenAPI.

Configuration avec des variables d'environnement
-----------------------------------------------

Chargez la configuration depuis l'environnement :

.. code-block:: python

    import os
    from flask_jeroboam import Jeroboam

    app = Jeroboam(__name__)
    app.config["JEROBOAM_TITLE"] = os.getenv("API_TITLE", "My API")
    app.config["JEROBOAM_REGISTER_OPENAPI"] = os.getenv("OPENAPI_ENABLED", "true").lower() == "true"

Puis définissez les variables d'environnement lors de l'exécution :

.. code-block:: bash

    API_TITLE="Production API" OPENAPI_ENABLED=false python app.py

Réponses d'erreur personnalisées
--------------------------------

Personnalisez la façon dont les erreurs de validation sont formatées :

.. code-block:: python

    from flask_jeroboam import Jeroboam
    from flask import jsonify

    app = Jeroboam(__name__)

    @app.errorhandler(422)
    def handle_validation_error(e):
        # Format personnalisé pour les erreurs de validation
        return jsonify({"errors": e.description}), 422

Les erreurs de validation retournent maintenant votre format personnalisé.

En-têtes de réponse
-------------------

Ajoutez des en-têtes à toutes les réponses ou à des endpoints spécifiques :

.. code-block:: python

    @app.after_request
    def add_headers(response):
        response.headers["X-API-Version"] = "1.0.0"
        return response

    @app.get("/items")
    def list_items():
        return fetch_items()

Toutes les réponses incluent l'en-tête personnalisé.

Mise en cache des réponses
--------------------------

Mettez en cache les réponses pour améliorer les performances :

.. code-block:: python

    from flask_caching import Cache

    app = Jeroboam(__name__)
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    @app.get("/items")
    @cache.cached(timeout=3600)
    def list_items():
        return fetch_all_items()

Ceci met en cache la réponse pendant 1 heure. La combinaison de Jeroboam avec les extensions Flask comme Flask-Caching fonctionne sans problème.

Configuration CORS
------------------

Activez CORS si votre API est accédée depuis un navigateur :

.. code-block:: python

    from flask_cors import CORS
    from flask_jeroboam import Jeroboam

    app = Jeroboam(__name__)
    CORS(app)

    @app.get("/items")
    def list_items():
        return fetch_items()

Jeroboam fonctionne avec les extensions Flask standard sans problème.

Journalisation et débogage
--------------------------

Activez le mode debug de Flask pour voir les traces d'erreur complètes :

.. code-block:: python

    app = Jeroboam(__name__)
    app.config["DEBUG"] = True
    app.run()

En mode debug, les erreurs de validation incluent les traces de pile et les détails. Désactivez en production.

Réglage des performances
-----------------------

Pour les APIs à fort trafic, considérez ces optimisations :

.. code-block:: python

    app = Jeroboam(__name__)

    # Désactiver la journalisation détaillée
    app.logger.setLevel("WARNING")

    # Utiliser un serveur WSGI de production
    app.run()

N'oubliez pas : utilisez Gunicorn, uWSGI ou similaire en production, pas ``app.run()``.

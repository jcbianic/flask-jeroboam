Visite Approfondie des Fonctionnalités
======================================

Dans cette partie de la documentation, nous couvrirons les fonctionnalités de **Flask-Jeroboam** en profondeur pour vous donner une compréhension solide du fonctionnement du paquet et de la meilleure façon de l'utiliser.

Le but de **Flask-Jeroboam** est de vous permettre de vous concentrer sur la logique métier de votre application web en fournissant un moyen facile de définir les interfaces entrantes et sortantes de vos endpoints. L'interface entrante définit comment les clients peuvent interagir avec vos endpoints, tandis que l'interface sortante définit ce que les clients peuvent en attendre.


Définir l'interface entrante des endpoints avec les arguments de fonction de vue
---------------------------------------------------------------------------------

Vous définissez l'analyse, la validation et l'injection de données entrantes dans vos fonctions de vue simplement à travers leurs arguments, en utilisant une combinaison d'annotations de type, de valeurs par défaut et de valeurs implicites sensées pour le rendre aussi concis que possible.

Apprenez :doc:`comment définir l'interface entrante de vos endpoints </fr/features/inbound_fr>` pour les rendre plus concis et robustes.

.. toctree::
    :maxdepth: 2

    inbound_fr

.. _Pydantic: https://pydantic-docs.helpmanual.io/

Définir l'interface sortante des endpoints avec les décorateurs de route
-------------------------------------------------------------------------

Vous définissez l'interface sortante de vos endpoints à travers les décorateurs de route, généralement en passant un ``response_model`` au décorateur. **Flask-Jeroboam** l'utilisera pour valider et sérialiser la valeur retournée par votre fonction de vue.

Apprenez :doc:`comment définir l'interface sortante de vos endpoints </fr/features/outbound_fr>` et soyez confiant que les données que vous renvoyez suivent le schéma que vous avez choisi pour elles.


.. toctree::
    :maxdepth: 2

    outbound_fr


AutoDocumentation OpenAPI
--------------------------

Alors que le but principal de la définition des interfaces entrantes et sortantes est de fournir l'analyse, la validation et la dé/sérialisation des données entrantes et sortantes pour votre endpoint au moment de l'exécution, elles offrent également une excellente opportunité de générer automatiquement une documentation `OpenAPI <https://swagger.io/specification/>`_ pour votre API.

Bien que la plupart se produise sans que vous ayez à écrire une seule ligne de code, apprenez :doc:`comment </fr/features/openapi_fr>` vous pouvez améliorer votre documentation.


.. toctree::
    :maxdepth: 2

    openapi_fr


Configuration
-------------

Les options de configuration vous permettent de:

- `Désactiver <configuration_fr.html#options-generales>`_ les fonctionnalités de haut niveau (par exemple, AutoDocumentation OpenAPI)
- Gérer les `Métadonnées OpenAPI <configuration_fr.html#metadonnees-openapi>`_ (par exemple, titre de l'API, version, description, etc.)

Nous les avons préfixées avec ``JEROBOAM_`` pour éviter les collisions de noms avec d'autres paquets.

.. toctree::
    :maxdepth: 2

    configuration_fr

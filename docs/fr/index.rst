.. rst-class:: hide-header

Bienvenue
=========

.. image:: ../_static/img/jeroboam_logo_with_text.png
    :alt: Flask-Jeroboam: un Flask durable pour des APIs de qualité.
    :width: 200px
    :align: center

Bienvenue dans la documentation de **Flask-Jeroboam**.

**Flask-Jeroboam** est une extension `Flask`_ inspirée de `FastAPI`_. Elle utilise `Pydantic`_
pour fournir une validation des données facile à configurer lors de l'analyse des requêtes et de la sérialisation des réponses,
ainsi que la génération automatique de documentation conforme à OpenAPI.

**Flask-Jeroboam** vous permet de profiter de la syntaxe élégante de FastAPI tout en restant dans l'écosystème Flask.
C'est parfait pour les développeurs qui aiment l'approche type-safe de FastAPI mais qui doivent travailler avec des applications Flask existantes
ou qui préfèrent la maturité et l'écosystème étendu de Flask.

Commencez avec :doc:`installation_fr`, puis lancez-vous directement avec notre :doc:`Guide de Démarrage </fr/getting_started_fr>`. Ensuite,
la :doc:`Visite Approfondie des Fonctionnalités </fr/features/index_fr>` plonge en profondeur dans l'utilisation de l'extension, tandis que
le :doc:`Tutoriel </fr/tutorial/index_fr>` vous guide à travers un exemple complet. Enfin, la section :doc:`API </api/index>` vous donne des détails sur les composants internes de l'extension.

.. note::
   Cette documentation suppose une certaine familiarité avec `Flask`_ et `Pydantic`_. Si vous êtes nouveau avec l'un ou l'autre, veuillez consulter leur documentation respective.
   Ils sont tous les deux fantastiques.

   - `Documentation Flask <https://flask.palletsprojects.com/>`_
   - `Documentation Pydantic <https://docs.pydantic.dev/>`_

.. _Flask: https://www.palletsprojects.com/p/flask/
.. _Pydantic: https://docs.pydantic.dev/
.. _FastAPI: https://fastapi.tiangolo.com/

Guide de l'Utilisateur
----------------------

Ce guide vous accompagnera dans l'utilisation de Flask-Jeroboam.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   installation_fr
   getting_started_fr
   features/index_fr
   tutorial/index_fr

Référence de l'API
------------------

Si vous recherchez des informations sur une fonction, une classe ou une
méthode spécifique, cette partie de la documentation est pour vous.

.. toctree::
   :maxdepth: 2

   ../api/index

Notes Supplémentaires
--------------------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   ../contributing
   ../codeofconduct
   ../license
   ../changes

Installation
============

Installer Flask-Jeroboam
-------------------------

Je publie **Flask-Jeroboam** sur `PyPI`_, l'index des paquets Python, et en tant que tel, il est facilement installable en utilisant l'une des commandes suivantes, selon votre outil de gestion des dépendances:

.. tabs::

   .. group-tab:: poetry

      .. code-block:: console

         $ poetry add flask-jeroboam

   .. group-tab:: pip

      .. code-block:: console

         $ pip install flask-jeroboam


Avec cette commande, vous avez installé **Flask-Jeroboam** avec ses deux dépendances directes, `Flask`_ et `Pydantic`_ ainsi que leur propre arbre de dépendances (:ref:`consultez-le ici <dependencies_fr>`).


.. note::
   Nous recommandons fortement d'installer **Flask-Jeroboam** dans un environnement virtuel. Si vous avez besoin de directives sur la façon de procéder, consultez la section :doc:`Configuration de l'Environnement <tutorial/setting_things_up_fr>` de notre tutoriel pour plus d'informations.

.. _dependencies_fr:

Dépendances
-----------

L'installation de **Flask-Jeroboam** installera automatiquement ces paquets avec leurs dépendances:

* `Flask`_ le gros du travail du framework web est toujours effectué par Flask.
* `Pydantic`_ pour fournir la validation des données en utilisant les annotations de type Python.

Ces deux dépendances directes viennent avec leur propre arbre de dépendances. Au total, vous aurez jusqu'à 9 nouveaux paquets installés.
Il existe une belle commande `poetry`_ pour explorer cet arbre. Voici comment:

.. code-block:: console

   $ poetry show flask-jeroboam --tree
   flask-jeroboam 0.1.0b0 Une extension Flask, inspirée de FastAPI qui utilise Pydantic pour fournir une validation des données facile à configurer pour l'analyse des requêtes et la sérialisation des réponses.
   ├── flask >=2.1.3,<3.0.0
   │   ├── click >=8.0
   │   │   └── colorama *
   │   ├── itsdangerous >=2.0
   │   ├── jinja2 >=3.0
   │   │   └── markupsafe >=2.0
   │   └── werkzeug >=2.2.2
   │       └── markupsafe >=2.1.1 (dépendance circulaire interrompue ici)
   └── pydantic >=1.10.2,<2.0.0
      └── typing-extensions >=4.2.0

.. _Flask: https://palletsprojects.com/p/flask/
.. _Pydantic: https://docs.pydantic.dev/

Tester votre installation
--------------------------

Assurons-nous que vous avez tout configuré correctement. Créez et ouvrez un fichier simple à la racine de votre projet: ``app.py``.

.. literalinclude:: ../../docs_src/readme/readme00.py
    :linenos:
    :language: python
    :lines: 2-

L'exécution de ce fichier devrait démarrer un serveur sur ``localhost:5000``. Vous pouvez appeler cet endpoint avec la commande ``curl 'http://localhost:5000/ping'``
ou directement dans votre navigateur en allant sur `http://localhost:5000/ping <http://localhost:5000/ping>`_. Si l'un ou l'autre répond "pong", votre installation est fonctionnelle, et vous êtes prêt à passer à notre :doc:`Guide de Démarrage </fr/getting_started_fr>`.

Dépannage
---------

Problèmes d'Installation Courants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Erreur d'importation: Aucun module nommé 'flask_jeroboam'**

Si vous rencontrez cette erreur après l'installation, assurez-vous que:

1. Vous utilisez le bon environnement Python (activez votre environnement virtuel)
2. Le paquet a été installé dans l'environnement actif: ``pip list | grep flask-jeroboam``
3. Vous utilisez la bonne instruction d'importation: ``from flask_jeroboam import Jeroboam``

**Conflits de Version**

Si vous rencontrez des conflits de version avec Flask ou Pydantic:

1. Vérifiez vos versions actuelles: ``pip show flask pydantic``
2. Assurez-vous que Flask >= 2.1.3 et Pydantic >= 1.10.2, < 2.0.0
3. Envisagez d'utiliser un nouvel environnement virtuel pour isoler les dépendances

**Problèmes d'Environnement Virtuel**

Si les paquets ne sont pas trouvés malgré l'installation:

.. code-block:: console

   $ python -m venv venv
   $ source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   $ pip install flask-jeroboam

Désinstaller Flask-Jeroboam
----------------------------

Retirer **Flask-Jeroboam** des dépendances de votre projet est aussi simple que de l'ajouter à votre projet:

.. tabs::

   .. group-tab:: poetry

      .. code-block:: bash

         $ poetry remove flask-jeroboam

   .. group-tab:: pip

      .. code-block:: bash

         $ pip uninstall flask-jeroboam


.. _poetry: https://python-poetry.org/
.. _pyenv: https://github.com/pyenv/pyenv
.. _PyPI: https://pypi.org/

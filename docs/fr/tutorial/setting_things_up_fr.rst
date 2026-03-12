Configuration des choses
========================

Si vous avez déjà compris la gestion des dépendances en Python, ignorez notre section suivante et allez directement à la :ref:`présentation <walkthrough>`. Sinon, :ref:`consultez-la <about_dep_management>` ou allez à la
:doc:`Documentation Vue d'ensemble </index>`.

.. _Flask: https://palletsprojects.com/p/flask/
.. _Pydantic: https://docs.pydantic.dev/

.. _about_dep_management:

À propos de la gestion des dépendances
--------------------------------------

Environnements virtuels
***********************

Les environnements virtuels sont essentiels pour isoler les dépendances de votre projet des packages système,
empêchant les conflits de version et fournissant la reproductibilité et la facilité de déploiement pour les contributeurs et vous-même.
De plus, il permet d'utiliser différentes versions de packages pour divers projets sur la même machine sans conflits.

C'est une bonne pratique, une pratique nécessaire même.

`uv`_ gère à la fois la gestion des versions de Python et les environnements virtuels dans un seul outil, et je vais vous montrer un exemple. Mais tout ce qui fonctionne déjà pour vous est bien.

.. _uv: https://docs.astral.sh/uv/
.. _pyenv: https://github.com/pyenv/pyenv
.. _PyPI: https://pypi.org/


Version de Python
*****************

Votre première dépendance, et la principale à cela, est votre installation de Python. Quand vous ignorez cela, vous finissez par utiliser l'installation Python par défaut de votre système, souvent obsolète.

La meilleure pratique est d'utiliser la dernière version stable de Python, qui est 3.13 au moment où j'écris ceci. :ref:`voir comment installer une version Python spécifique <install-install-python>`. L'équipe principale de Python fait un travail fantastique, et ce serait dommage de manquer tous les améliorations qu'ils apportent au jeu à chaque sortie.

Cela dit, **Flask-Jeroboam** supporte Python 3.10 et plus. Cela signifie que le pipeline CI/CD
teste le package de Python 3.10 à la version la plus récente. À mesure que les versions de Python atteignent leur fin de vie, nous cesserons de les prendre en charge mais resterons à jour avec les versions les plus récentes.

.. _walkthrough:

Une présentation d'installation complète
-----------------------------------------

Pour suivre cette section, vous devez avoir `uv`_ installé sur votre système. Si ce n'est pas le cas, suivez les `instructions d'installation de uv <https://docs.astral.sh/uv/getting-started/installation/>`_.


Installez la version la plus récente de Python
**********************************************

.. _install-install-python:

Premièrement, vous voulez choisir une version Python spécifique à installer et activer. Comme dit ci-dessus, la dernière version stable est votre meilleure option.
Installons-la en utilisant `uv`_ :

.. code-block:: bash

   # Installez la version la plus récente de Python
   $ uv python install 3.13
   # Vérifiez si cela a fonctionné
   $ uv run --python 3.13 python --version
   Python 3.13.x

Une fois que vous avez sécurisé la version Python correcte, vous pouvez créer un environnement virtuel pour votre projet.

Créez un environnement
**********************

.. _install-create-env:

`uv`_ peut initialiser un nouveau projet avec un ``pyproject.toml`` et un environnement virtuel en une seule commande :

.. code-block:: bash

   # Créez un répertoire racine, accédez-y et initialisez le projet
   $ mkdir jeroboam-demo && cd jeroboam-demo
   $ uv init --python 3.13


.. _install-activate-env:

Activez l'environnement
***********************

uv crée et gère l'environnement virtuel pour vous automatiquement. Vous pouvez l'activer explicitement si nécessaire :

.. code-block:: bash

   $ source .venv/bin/activate

Ou simplement préfixez les commandes avec ``uv run`` pour les exécuter à l'intérieur de l'environnement du projet sans l'activer :

.. code-block:: bash

   $ uv run python

Ajoutez et installez Flask-Jeroboam dans votre environnement
***********************************************************

Maintenant, vous êtes prêt à installer **Flask-Jeroboam**. Comme nous l'avons vu avant, cela ressemblerait à ceci :

.. code-block:: bash

   $ uv add flask-jeroboam

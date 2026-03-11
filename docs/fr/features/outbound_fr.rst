Interface sortante et paramètres des décorateurs de route
=========================================================

Vous avez vu dans la :doc:`section précédente </fr/features/inbound_fr>` comment définir l'argument de vos fonctions de vue pour définir l'interface entrante de votre endpoint. Maintenant, nous nous concentrerons sur la définition de l'interface sortante avec les arguments nommés à vos décorateurs de route.

Par interface sortante, nous entendons la forme de la réponse que votre serveur renvoie quand il est frappé par le client. Elle englobe à la fois le :ref:`schéma de charge utile <response_model>` de la réponse et le :ref:`code de statut <status_code>`.

.. _response_model:

Modèle de réponse
*****************

Le modèle de réponse définit le schéma de charge utile de votre réponse, ou en d'autres termes, la forme des données que vous renvoyez au client. La façon préférée de le faire est de passer un BaseModel pydantic au paramètre ``response_model`` de votre décorateur de route. Alternativement, la valeur de retour de votre fonction de vue peut implicitement définir ce modèle de réponse.

.. _add_explicit_response_model:

Modèle de réponse explicite
---------------------------

La façon la plus directe de définir l'interface sortante de votre endpoint est d'utiliser l'argument ``response_model`` de votre décorateur de route comme ceci ``@app.get("/tasks/<int:task_id>", response_model=Task)``. Cet argument prend un modèle pydantic comme valeur et l'utilisera pour valider et sérialiser les données renvoyées par votre fonction de vue.

Disons que vous avez un endpoint ``GET`` qui retourne une ``Task``. Tout d'abord, nous définissons un modèle ``Task``, héritant de ``BaseModel`` pydantic. Notre modèle ``Task`` a trois champs : ``id``, ``name``, et ``description``. Le champ ``description`` est optionnel et a une valeur par défaut de ``Just here to make a point.`` qui nous aidera à comprendre la mécanique plus tard.

.. literalinclude:: /../docs_src/features/outbound.py
  :linenos:
  :language: python
  :lines: 2-7,8-13,14-19,29-33
  :emphasize-lines: 3,4,13-16


Ensuite à la ligne 19, nous la donnons à l'argument ``response_model`` de notre décorateur de route à la ligne 19. Notez qu'à la ligne 21 nous retournons seulement un dictionnaire avec les champs ``id`` et ``name``. Le champ ``description`` manque, mais c'est d'accord. **Flask-Jeroboam** l'ajoutera pour nous via le modèle ``Task``.

.. literalinclude:: /../docs_src/features/outbound.py
  :linenos:
  :language: python
  :lines: 2-7,8-13,14-19,29-33
  :emphasize-lines: 19, 21

**Flask-Jeroboam** prend la valeur retournée par la fonction de vue et la verse dans votre reponse_model, valide les données, les sérialise en JSON, et enfin les enveloppe dans un objet ``Response`` avant de les remettre à Flask.

Testons-le :

.. code-block:: bash

    $ curl http://localhost:5000/tasks/42
    {"id": 42, "name": "Find the answer.", "description": "Just here to make a point."}

Comme vous pouvez le voir, l'endpoint utilise les données retournées par cette fonction de vue mais ajoute également la valeur par défaut du champ ``description``. C'est parce que **Flask-Jeroboam** utilise le modèle ``Task`` pour valider les données retournées par la fonction de vue. Elle ajoutera tous les champs manquants et les remplira avec leurs valeurs par défaut.

Pour le démontrer, définissons un autre endpoint qui retourne le même dictionnaire sans l'argument ``response_model``.

.. literalinclude:: /../docs_src/features/outbound.py
  :linenos:
  :language: python
  :lines: 7,8-13,34-38
  :emphasize-lines: 8

et testons-le :

.. code-block:: bash

    $ curl http://localhost:5000/tasks/42/no_response_model
    {"id":42,"name":"I'm from the dictionary."}

Cette fois, Flask reçoit un dictionnaire simple. Il n'ajoutera aucune valeur par défaut ni n'essaiera de la valider contre aucun schéma. Il la retourne simplement.

Les BaseModels pydantic sont une façon convaincante de définir un schéma complexe. Elles sont hautement réutilisables et ont prouvé d'être un excellent outil pour définir des modèles de données. Par exemple, vous pouvez imbriquer des modèles, en assignant un BaseModel comme le type d'un champ de modèle parent. Vous pouvez aussi définir des règles de validation, comme des valeurs minimales et maximales, des motifs regex... Vous pouvez même définir des règles de validation personnalisées. Pour plus d'informations sur les modèles pydantic, consultez la `documentation pydantic <https://docs.pydantic.dev/>`_.

Alternativement aux déclarations explicites, vous pouvez également laisser **Flask-Jeroboam** déduire le modèle de réponse des valeurs de retour de votre fonction de vue.

Modèle de réponse implicite
---------------------------

**Flask-Jeroboam** peut également dériver votre modèle de réponse à partir du type de retour de la fonction de vue, mais il doit provenir d'une annotation. Dans les exemples suivants, le premier endpoint fonctionnera de manière similaire à celui de la section précédente, mais le second lèvera une erreur car Flask ne sait pas quoi faire avec l'objet ``Task``.

.. literalinclude:: /../docs_src/features/outbound.py
  :linenos:
  :language: python
  :lines: 2-7,8-13,14-19,39-48
  :emphasize-lines: 20,25

Testons-le.

.. code-block:: bash

    $ curl http://localhost:5000/tasks/42/implicit_from_annotation
    {"id": 42, "name": "Implicit from Annotation", "description": "Just here to make a point."}%
    $ curl -w 'Status Code: %{http_code}\n' http://localhost:5000/tasks/42/implicit_no_annotation
    {"message":"Internal Error"}
    Status Code: 500

Cependant, explicite est mieux qu'implicite, donc vous devez préférer l'argument ``response_model`` à cette approche. De plus, créer l'instance ``Task`` semble inutilement verbeux car, comme vu avant, vous pouvez retourner directement le dictionnaire. En parlant de cela, regardons les valeurs de retour autorisées.

Valeurs de retour autorisées
----------------------------

Quand un modèle de réponse est défini, **Flask-Jeroboam** peut accepter les éléments suivants de la part des valeurs retournées par les fonctions de vue :

- un dictionnaire
- une instance de dataclass
- une liste
- une instance de modèle pydantic
- une instance de réponse Flask (bien qu'elle ignorera la partie sérialisation de son algorithme)

Notez qu'en plus des éléments ci-dessus, vous pouvez également retourner un tuple de la forme ``(body, status_code)``, ``(body, headers)``, ``(body, status_code, headers)``. Le code de statut et les en-têtes seront utilisés dans la réponse. Notamment, le :ref:`status_code` sera remplacé.

L'éteindre
-----------

Si vous ne voulez pas utiliser les fonctionnalités sortantes de **Flask-Jeroboam**, éteignez-la en définissant l'argument ``response_model`` à ``None``. Cela fera en sorte que **Flask-Jeroboam** ignore l'interface sortante de votre endpoint.

.. literalinclude:: /../docs_src/features/outbound.py
  :linenos:
  :language: python
  :lines: 7,8-13,49-53
  :emphasize-lines: 8

L'endpoint fonctionne toujours.

.. code-block:: bash

    $ curl http://localhost:5000/tasks/42/response_model_off
    {"id": 1, "name": "Response Model is off."}

Ensuite, regardons un autre aspect de l'interface sortante d'un endpoint : le code de statut de succès.

.. _status_code:

Code de statut
**************

**Flask-Jeroboam** soutient à la fois les codes de statut au moment de l'enregistrement et les codes de statut des valeurs de retour.

Code de statut au moment de l'enregistrement
---------------------------------------------

Quand vous enregistrez votre fonction de vue, **Flask-Jeroboam** essaiera de résoudre le code de statut de la réponse réussie. Il regardera d'abord le paramètre `status_code` du décorateur de route, puis la valeur définie par le paquet pour le verbe HTTP du décorateur de route, et enfin l'attribut code de statut de la classe de réponse, si présente.

.. warning::

    **Flask-Jeroboam** ne sera en mesure d'utiliser ce code de statut au *moment de l'enregistrement* que dans la documentation OpenAPI de votre opération.

Nous utilisons les valeurs par défaut suivantes pour chaque verbe HTTP :

- ``GET``: 200
- ``HEAD``: 200
- ``POST``: 201
- ``PUT``: 201
- ``DELETE``: 204
- ``CONNECT``: 200
- ``OPTIONS``: 200
- ``TRACE``: 200
- ``PATCH``: 200

Comme vous pouvez le voir, vous n'aurez pas besoin de définir un code de statut explicite la plupart du temps.

Par exemple, l'endpoint suivant aura un code de statut au *moment de l'enregistrement* de 201. Comme la fonction de vue ne retourne pas de code de statut, une requête put réussie nous donnera un code de statut 201.

.. code-block:: python

    @app.put("/tasks", response_model=TaskOut)
    def create_task(task: TaskIn):
        return {"task_id": task.id}

.. code-block:: bash

    $ curl -w 'Status Code: %{http_code}\n' -PUT http://localhost:5000/tasks -d '{"name": "My Task"}'
    Status Code: 201
    {"task_id": 1}

Maintenant, disons que nous définissons un deuxième endpoint qui prend une tâche et commence à l'exécuter. Dans ce cas, vous pourriez vouloir remplacer le défaut (``201``) par un ``202`` plus approprié signifiant "Accepté mais pas fait" (voir `RFC 7231 <https://tools.ietf.org/html/rfc7231#section-6.3.3>`_). Vous le feriez de cette façon :

.. code-block:: python

    @app.put("/tasks", response_model=TaskOut, status_code=202)
    def create_task(task: TaskIn):
        # Save the Task and Launch it
        return {"task_id": task.id}


Cette fois, quand nous faisons une requête réussie, nous obtiendrons un code de statut ``202`` dans la réponse.

.. code-block:: bash

    $ curl -PUT http://localhost:5000/tasks -d '{"name": "My Task"}'
    Status Code: 202
    {"task_id": 1}


Code de statut de la valeur de retour
--------------------------------------

**Flask-Jeroboam** supporte également le retour d'un code de statut comme un tuple, tout comme dans **Flask**. Il remplacera le code de statut au *moment de l'enregistrement*, mais **Flask-Jeroboam** ne sera pas en mesure d'ajuster la documentation. Cela pourrait entraîner des incohérences entre votre documentation et le comportement réel de l'API.

Si nous revisiting l'exemple précédent, vous pouviez obtenir le même résultat de *demande-traitement* avec le code suivant :

.. code-block:: python

    @app.put("/tasks", response_model=TaskOut)
    def create_task(task: TaskIn):
        # Save the Task and Launch it
        return {"task_id": task.id}, 202


La requête PUT réussie nous donnera toujours un code de statut ``202`` dans la réponse.

.. code-block:: bash

    $ curl -PUT http://localhost:5000/tasks -d '{"name": "My Task"}'
    Status Code: 202
    {"task_id": 1}

Cependant, la documentation résultante serait différente. Voir :doc:`openapi_fr` pour plus de détails.


En résumé, quand **Flask-Jeroboam** traite la requête, il utilisera le code de statut déduit au moment de l'enregistrement sauf si la fonction de vue retourne une valeur contenant un code de statut.

Si vous utilisez la documentation OpenAPI, la façon préférée est d'ajouter un code de statut au *moment de l'enregistrement* pour garantir la cohérence entre votre documentation et votre API. Le code de statut retourné est également soutenu pour éviter de casser le code existant.

Aide-mémoire
*************

- Pour définir le schéma de charge utile de vos réponses, vous passez un BaseModel pydantic à l'argument nommé du décorateur de route ``response_model`` (par ex. ``@app.get("/task/<int:id>", response_model=TaskOut)``).
- Si vous voulez remplacer le code de statut implicite, vous pouvez utiliser l'argument nommé ``status_code`` (par ex. ``@app.put("/task/<int:id>/run", status_code=202)``).
- Si vous voulez désactiver le modèle de réponse implicite, utilisez l'argument nommé ``response_model=None``. (par ex. ``@app.get("/task/<int:id>", response_model=None)``)

Ensuite, regardez comment tirer le meilleur de la génération automatique de la documentation :doc:`OpenAPI <openapi_fr>`.

.. rubric:: Fonctionnalités prévues

- Vues basées sur des modèles (`<https://github.com/jcbianic/flask-jeroboam/issues/105>`_)
- Prendre en charge les options de sérialisation (par ex. exclude_unset) (`<https://github.com/jcbianic/flask-jeroboam/issues/105>`_)

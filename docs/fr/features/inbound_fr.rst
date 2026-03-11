Interface entrante et arguments de fonction de vue
====================================================

Nous nous concentrerons ici sur la façon d'utiliser les arguments de vos fonctions de vue pour définir l'interface entrante d'un endpoint. Par interface entrante, nous entendons les données qu'un client peut envoyer au serveur et comment.

Avec **Flask-Jeroboam**, vous utilisez une combinaison de hints de type et de valeurs par défaut sur les arguments de votre fonction de vue pour définir l'interface entrante de vos endpoints. Cette fonctionnalité vous permet de déléguer l'analyse, la validation et l'injection de données entrantes à l'extension et de vous concentrer sur la logique métier de vos endpoints.

**Flask-Jeroboam** traitera les données entrantes en fonction de leur emplacement, leur type et les options de validation supplémentaires. L'emplacement fait référence à la façon dont le client transmet les données sur une requête HTTP entrante (par ex. chaînes de requête, en-têtes, corps de la requête...). Le type définit la forme ou le schéma attendu des données entrantes. De plus, vous pouvez spécifier des options de validation supplémentaires.

Emplacement
-----------

Le concept d'emplacement fait référence à la façon dont le client transmet les données sur une requête HTTP entrante. Tout d'abord, nous regarderons les sept emplacements possibles. Ensuite, nous examinerons l'emplacement implicite que **Flask-Jeroboam** assumera, et enfin comment vous pouvez explicitement définir l'emplacement de chaque argument de vos fonctions de vue.


Que sont les emplacements
~~~~~~~~~~~~~~~~~~~~~~~~~

Il existe plusieurs façons de transmettre des données avec une requête HTTP. Flask et Werkzeug analysent déjà les données brutes entrantes de la requête pour remplir les membres de l'objet ``request`` en conséquence. Définir l'emplacement d'un argument est une façon de dire à **Flask-Jeroboam** quel membre du ``request`` utiliser pour récupérer les données entrantes et les injecter dans vos fonctions de vue.

Il existe sept emplacements possibles pour les arguments de fonctions de vue.

- Quatre paramètres :

  * ``PATH``: Les paramètres de chemin sont les parties dynamiques d'une URL trouvées avant tout séparateur ``?`` (par ex. ``/items/12``). Ils sont généralement utilisés pour transmettre des identifiants. Flask les injecte déjà dans votre fonction de vue.
  * ``QUERY``: Les chaînes de requête sont des paires clé-valeur séparées par des signes égaux trouvées dans la partie de l'URL après le séparateur ``?`` (par ex. ``?page=1``). Elles servent à diverses fins. Nous les récupérons à partir de ``request.args`` de Flask.
  * ``HEADER``: Les paramètres d'en-tête sont des champs destinés à transmettre un contexte supplémentaire ou des métadonnées sur la requête au serveur. Ce sont des paires clé-valeur séparées par deux points comme ceci ``X-My-Header: 42``. Nous les récupérons à partir de ``request.headers`` de Flask.
  * ``COOKIE``: Les cookies sont stockés côté client pour suivre un état dans un protocole sans état. Ils ressemblent à ceci ``Cookie: username=john``, et nous les récupérons à partir de ``request.cookies`` de Flask.

- Trois variantes du corps de la requête :

  * ``BODY``: Le corps de la requête d'une requête HTTP est le contenu optionnel de la requête. Les requêtes de récupération de ressources [#3]_ n'en ont généralement pas. Le corps de la requête a une propriété content-type (comme : ``application/json``) qui donne au serveur une indication sur la façon de les analyser. Nous récupérons le corps de la requête à partir de ``request.data`` de Flask (ou ``request.json`` lorsque son mimetype est ``application/json``).
  * ``FORM``: Un corps de requête avec une valeur content-type de ``application/x-www-form-urlencoded``. Nous récupérons les données à partir de ``request.form`` de Flask.
  * ``FILE``: Corps de requête avec un enctype de ``multipart/form-data`` et nous récupérons les données à partir de ``request.files`` de Flask.

.. [#3] Comme ``GET``, ``OPTIONS``, ``HEAD``

Résolution de l'emplacement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

La plupart du temps, vous n'aurez pas à définir explicitement l'emplacement de vos arguments, grâce au mécanisme d'emplacement implicite de **Flask-Jeroboam**. Cependant, vous pouvez également définir explicitement l'emplacement pour chaque argument de vos fonctions de vue en utilisant des fonctions spéciales sur les valeurs par défaut de vos arguments.

Emplacement implicite
*********************

Nous pouvons réduire l'heuristique de **Flask-Jeroboam** pour déterminer l'emplacement d'un argument à quelques règles simples :

- le nom de l'argument sera vérifié par rapport aux noms des paramètres de chemin de la règle d'endpoint
- les arguments des verbes de récupération de ressources sont supposés être des paramètres ``QUERY``
- les arguments des verbes de création de ressources sont supposés être des paramètres ``BODY``

.. warning::
  Ceci est légèrement différent de l'heuristique de **FastAPI**, où les valeurs singulières sont supposées être des paramètres ``QUERY`` peu importe le verbe, et les modèles pydantic sont supposés être des paramètres ``BODY``.

Outre les paramètres de chemin, **Flask-Jeroboam** dérive l'emplacement implicite d'un argument du verbe HTTP de votre fonction de vue, basé sur l'hypothèse que pour une requête ``GET``, le client transmet généralement les paramètres via la chaîne de requête et que pour les requêtes ``PUT`` et ``POST`` le client utilisera principalement le corps de la requête.

Observez les endpoints en surbrillance ci-dessous—le premier utilise ``GET`` (emplacement ``QUERY`` implicite) et le second utilise ``POST`` (emplacement ``BODY`` implicite) :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 11-13,31-33
  :emphasize-lines: 1,4

Si vous exécutez le fichier ci-dessus, vous pouvez le tester. L'endpoint ``/implicit_location_is_query_string`` attendra un paramètre page dans la chaîne de requête.

.. code-block:: bash

  $ curl 'localhost:5000/implicit_location_is_query_string?page=42'
  Received Page Argument is : 42

tandis que l'endpoint ``/implicit_location_is_body`` attendra un champ page dans le corps de la requête.

.. code-block:: bash

  $ curl -X POST 'localhost:5000/implicit_location_is_body' -d '{"page": 42}' -H "Content-Type: application/json"
  Received Page Argument is : 42

Bien que les deux fonctions de vue aient reçu les mêmes valeurs de paramètre, remarquez que nous construisons notre requête différemment en hébergeant les paramètres à deux emplacements différents.

De plus, **Flask-Jeroboam** détectera automatiquement les paramètres de chemin. Notez la route surlignée et la fonction ci-dessous—la ``<int:id>`` dans la règle d'URL et le paramètre ``id`` dans la signature de la fonction correspondent automatiquement.

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 41-43
  :emphasize-lines: 1,2

Vous pouvez le tester :

.. code-block:: bash

  $ curl 'localhost:5000/item/42/implicit'
  Received id Argument is : 42

Cela fonctionne également avec d'autres verbes HTTP. Notez l'endpoint ``POST`` en surbrillance ci-dessous—il a la même gestion des paramètres de chemin malgré l'utilisation d'un verbe HTTP différent :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 41-43,46-48
  :emphasize-lines: 4,5

.. code-block:: bash

  $ curl -X POST 'localhost:5000/item/42/implicit'
  Received id Argument is : 42

.. note::
    Ce mécanisme d'emplacement implicite est l'une des raisons pour lesquelles le décorateur de méthode (@app.get/put/post VS @app.route) est la façon préférée de registrer une fonction de vue dans **Flask-Jeroboam**. Il applique la bonne pratique d'avoir un seul verbe HTTP par fonction de vue. Les fonctions de vue attribuées à plus d'un verbe HTTP ont tendance à être divisées en deux branches largement indépendantes, ce qui réduit leur lisibilité.

Bien que l'emplacement implicite couvrira la plupart des cas, vous pouvez également les définir explicitement.

Emplacements explicites
***********************

Pour définir des emplacements explicites, vous devez utiliser l'une des fonctions spéciales de **Flask-Jeroboam** (``Path``, ``Query``, ``Cookie``, ``Header``, ``Body``, ``Form`` ou ``File``) pour assigner des valeurs par défaut à vos arguments.

Notez les sections surlignées ci-dessous—l'endpoint ``GET`` implicite utilise un paramètre ordinaire, tandis que la version explicite utilise ``Query()``. Les deux se comportent de manière identique :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 11-13,16-18
  :emphasize-lines: 2,5

La même équivalence s'applique aux requêtes ``POST`` et ``PUT``. Regardez les exemples en surbrillance ci-dessous—les emplacements implicites et explicites produisent le même comportement :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 5,31-33,36-38
  :emphasize-lines: 3,6

Testons-le.

.. code-block:: bash
  :linenos:

  $ curl 'localhost:5000/implicit_location_is_query_string?page=42'
  Received Page Argument is : 42
  $ curl 'localhost:5000/explicit_location_is_query_string?page=42'
  Received Page Argument is : 42
  $ curl -X POST 'localhost:5000/implicit_location_is_body' -d '{"page": 42}' -H "Content-Type: application/json"
  Received Page Argument is : 42
  $ curl -X POST 'localhost:5000/explicit_location_is_body' -d '{"page": 42}' -H "Content-Type: application/json"
  Received Page Argument is : 42

Vous pouvez également mélanger les emplacements implicites et explicites. Regardez le code surligné ci-dessous—le premier endpoint utilise ``Query()`` et ``Cookie()`` explicites, tandis que le second utilise des emplacements implicites :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 5,21-23,26-28
  :emphasize-lines: 3,6

Testons-le.

.. code-block:: bash
  :linenos:

  $ curl 'localhost:5000/explicit_location_is_query_string_and_cookie?page=42' --cookie "username=john"
  Received Page Argument is : 42. Username is : john
  $ curl 'localhost:5000/implicit_and_explicit?page=42' --cookie "username=john"
  Received Page Argument is : 42. Username is : john

.. note::
  Les linters comme Flake8 se plaindront probablement de faire un appel de fonction dans un argument par défaut. Bien que ce soit un bon conseil, cela ne causera aucun effet indésirable dans ce cas particulier. Vous devriez envisager de désactiver les avertissements ``B008`` pour les fichiers dans lesquels vous définissez vos fonctions de vue.

Assigner des valeurs par défaut
*******************************

Comme vous l'avez peut-être deviné, les fonctions spéciales détournent le mécanisme de valeur par défaut pour vous permettre de définir facilement un emplacement explicite pour vos arguments. En conséquence, leur valeur renvoyée ne sera pas utilisée comme solution de secours quand le client ne fournit pas d'argument. En fait, jusqu'à présent, tous les arguments que nous avons définis sont implicitement requis car ils n'ont pas de valeurs par défaut pour se replier quand la requête ne les fournit pas.

Ne me croyez pas sur parole, testons-le sur l'endpoint ``/implicit_location_is_query_string`` précédemment défini.

.. code-block:: bash

  $ curl -w 'Status Code: %{http_code}\n' 'localhost:5000/implicit_location_is_query_string'
  {"detail":[{"loc":["query","page"],"msg":"field required","type":"value_error.missing"}]}
  Status Code: 400

Nous avons reçu une réponse 400 Bad Request car nous n'avons pas fourni le paramètre requis page dans notre chaîne de requête. Et si nous voulions définir une valeur par défaut de 1 pour le paramètre page ? Il y a deux façons de le faire :

-  Avec l'emplacement implicite, définissez la valeur par défaut normalement dans la signature de la fonction (par ex., ``page: int = 1``).
-  Avec l'emplacement explicite, passez la valeur par défaut comme premier argument à la fonction d'emplacement (par ex., ``page: int = Query(1)``).

Regardez les exemples surlignés ci-dessous :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 56-58,61-63
  :emphasize-lines: 2,5

Testons-le.

.. code-block:: bash
  :linenos:

  $ curl 'localhost:5000/implicit_location_with_default_value'
  Received Page Argument is : 1
  $ curl 'localhost:5000/implicit_location_with_default_value?page=42'
  Received Page Argument is : 42
  $ curl 'localhost:5000/explicit_location_with_default_value'
  Received Page Argument is : 1
  $ curl 'localhost:5000/explicit_location_with_default_value?page=42'
  Received Page Argument is : 42

La valeur par défaut est correctement insérée quand vous ne fournissez pas le paramètre dans la chaîne de requête pour l'un ou l'autre endpoint. Le serveur retourne une réponse valide ce qui signifie que le paramètre page n'est plus requis.

Les fonctions spéciales fournissent également un moyen de définir des options de validation supplémentaires, mais d'abord, examinons de plus près la définition de la deuxième partie de nos arguments d'entrée : le type.

Type
----

Le type fait référence à la forme ou au schéma des données que vous attendez. Vous pouvez assigner un type à un argument en utilisant des hints de type. Les types peuvent être des types intégrés à Python (par ex. ``str``, ``int``, ``float``), des sous-classes de ``BaseModel`` pydantic ou un conteneur des deux précédents (par ex. ``List[str]``)

En plus d'utiliser des hints de type, vous pouvez également utiliser le premier argument de fonctions spéciales comme ``Query``.

Regardez la définition du modèle ``Item`` en surbrillance ci-dessous :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 3,5,66-68
  :emphasize-lines: 3,4,5

Maintenant voyez comment ce modèle est utilisé. La définition de la fonction surlignée ci-dessous montre différents modèles de type :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 3,5,66-68,71-79
  :emphasize-lines: 7

Testons-le.

.. code-block:: bash

  $ curl 'localhost:5000/defining_type_with_type_hints?page=42&search=foo&search=bar&price=42.42&name=test&count=3'
  Received arguments are :
  page : 42
  search : ['foo', 'bar']
  price : 42.42
  item : name='test' count=3

Vous remarquerez que nous n'avons pas essayé de passer un dictionnaire à un champ ``item`` à la chaîne de requête. Au lieu de cela, nous avons passé deux arguments, ``name`` et ``count``, correspondant aux champs internes de Item. Les chaînes de requête ne sont généralement pas une bonne façon de transmettre des structures de données imbriquées. Si vous avez besoin de transmettre une structure de données complexe, utilisez un emplacement différent comme un corps JSON ou un formulaire.

Avec les corps de requête, vous pouvez choisir entre des arguments incorporés ou plats.

.. note::
  Les hints de type ne sont pas initialement censés fournir une fonctionnalité d'exécution. Mais ce principe a été lancé par pydantic et repris plus tard par FastAPI. Nous sommes donc en bonne compagnie.

Options de validation
---------------------

Les arguments de fonction de vue sont essentiellement des champs de modèle pydantic, ce qui signifie que quand vous les définissez, vous pouvez exploiter chaque fonction de validation que pydantic offre sur les champs de modèle.

Pour les types de nombres par exemple, vous pouvez ajouter des valeurs ``ge`` (signifiant supérieur ou égal à) ou ``lt`` (inférieur à) pour définir des conditions de validation sur vos paramètres.

Regardez l'exemple surligné ci-dessous—remarquez la contrainte ``ge=1`` :

.. literalinclude:: /../docs_src/features/inbound.py
  :linenos:
  :language: python
  :lines: 82-84
  :emphasize-lines: 2

Regardons ce qui se passe quand nous passons une valeur de page de 0. Notez que 0 est un int valide, mais il n'est pas supérieur ou égal à 1.

.. code-block:: bash

  $ curl -w 'Status Code: %{http_code}\n' 'localhost:5000/argument_with_validation?page=0'
  {"detail":[{"ctx":{"limit_value":1},"loc":["query","page"],"msg":"ensure this value is greater than or equal to 1","type":"value_error.number.not_ge"}]}
  Status Code: 400

Le serveur retourne un code de statut 400 avec un corps vous donnant une direction sur l'erreur : il n'a pas passé la validation ``ge=1``.

.. note::
  Bien que vous puissiez le faire en utilisant une fonction spéciale, je crois que cela entraînerait un code de signature de fonction de vue gonflé dans de nombreux cas. Au-delà de quelques arguments élémentaires, ma préférence va à la définition d'un BaseModel pydantic d'abord avec des champs complets et des conditions de validation sur chacun d'eux, puis utiliser ce BaseModel comme un hint de type pour définir la forme d'un argument d'entrée.

Aide-mémoire
-------------

En résumé, vos arguments d'entrée sont définis par :

- leur emplacement : défini soit implicitement, soit explicitement en utilisant des fonctions spéciales comme valeurs par défaut (``page:int = Query()``)
- leurs valeurs par défaut optionnelles : définies soit comme des valeurs par défaut régulières ``page:int = 1`` soit explicitement en utilisant des fonctions spéciales (``page:int = Query(1)``)
- leur type : en utilisant un hint de type (``page: int``) ou le premier argument de fonctions spéciales (``page = Query(int)``)
- leurs options de validation optionnelles : en passant des arguments nommés supplémentaires aux appels de fonctions spéciales (``page:int = Query(ge=1)``)

Ensuite, consultez :doc:`comment définir les interfaces sortantes <outbound_fr>`.

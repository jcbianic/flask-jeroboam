Documentation automatique d'OpenAPI
====================================

En plus de fournir des fonctionnalités de traitement des demandes, la définition d'interfaces entrantes et sortantes vous permet de bénéficier d'une documentation générée automatiquement avec peu d'effort supplémentaire. C'est aussi simple que d'appeler la méthode ``init_app`` sur votre instance d'application Jeroboam. Cela enregistrera un blueprint interne avec deux endpoints. L'un sert la documentation OpenAPI au format JSON, et l'autre sert l'interface utilisateur Swagger.

.. literalinclude:: /../docs_src/features/openapi_examples/01_init_app.py
  :linenos:
  :language: python
  :lines: 3-5


Vous pouvez la consulter à `<localhost:5000/openapi>`_ et `<localhost:5000/docs>`_.

L'éteindre
----------

Si vous ne voulez pas utiliser la fonction de documentation automatique, éteignez-la en définissant le drapeau de configuration ``JEROBOAM_REGISTER_OPENAPI`` à ``False``.

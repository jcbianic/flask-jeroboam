Configuration
=============

Les options de configuration vous permettent :

- De refuser les fonctionnalités de haut niveau (par ex. la documentation automatique OpenAPI)
- De gérer les métadonnées OpenAPI (par ex. titre de l'API, version, description, etc.)

Elles sont préfixées avec ``JEROBOAM_`` pour éviter les collisions de noms avec d'autres packages.


Contenu
~~~~~~~

- `Options générales`_

  * `JEROBOAM_REGISTER_OPENAPI`_
  * `JEROBOAM_REGISTER_ERROR_HANDLERS`_

- `Métadonnées OpenAPI`_

  * `JEROBOAM_TITLE`_
  * `JEROBOAM_VERSION`_
  * `JEROBOAM_DESCRIPTION`_
  * `JEROBOAM_TERMS_OF_SERVICE`_
  * `JEROBOAM_CONTACT`_
  * `JEROBOAM_LICENCE_INFO`_
  * `JEROBOAM_OPENAPI_VERSION`_
  * `JEROBOAM_SERVERS`_
  * `JEROBOAM_OPENAPI_URL`_

Options générales
~~~~~~~~~~~~~~~~~

Les options générales vous permettent de refuser certaines des fonctionnalités de **Flask-Jeroboam**, au cas où vous ne les auriez pas besoin, ou si vous avez besoin de les personnaliser, ou si elles interfèrent avec le reste de votre application.

.. _JEROBOAM_REGISTER_OPENAPI:
.. py:data:: JEROBOAM_REGISTER_OPENAPI

    Il contrôle si le Blueprint OpenAPI sera enregistré quand vous appelez la méthode ``init_app`` sur l'instance d'application.

    Mettez-le à ``False`` si vous ne voulez pas que le Blueprint OpenAPI soit enregistré ou si vous voulez brancher vos propres fonctions de vue pour servir les fonctionnalités OpenAPI.

    Par défaut : ``True``


.. _JEROBOAM_REGISTER_ERROR_HANDLERS:
.. py:data:: JEROBOAM_REGISTER_ERROR_HANDLERS

    Il contrôle si les gestionnaires d'erreurs définis par le package des exceptions de **Flask-Jeroboam** seront enregistrés quand vous appelez la méthode ``init_app`` sur l'instance d'application.

    Mettez-le à ``False`` si vous ne voulez pas que les gestionnaires d'erreurs définis par le package soient enregistrés. Notez que si vous le faites, vous devrez définir vos propres gestionnaires d'erreurs pour les exceptions suivantes : ``RessourceNotFound``, ``InvalidRequest`` et ``ResponseValidationError``.

    Par défaut : ``True``


Métadonnées OpenAPI
~~~~~~~~~~~~~~~~~~~

Les options de configuration des métadonnées OpenAPI vous permettent de contrôler les métadonnées de votre documentation OpenAPI, comme son titre, ses versions, les informations de contact, etc... Définir ces options est optionnel, ce qui signifie que vous aurez une page OpenAPI opérationnelle avant de définir ces options.

.. _JEROBOAM_TITLE:
.. py:data:: JEROBOAM_TITLE

    Le titre de votre API. Il apparaîtra comme le titre principal de votre page de documentation OpenAPI.

    Par défaut : ``app.name``


.. _JEROBOAM_VERSION:
.. py:data:: JEROBOAM_VERSION

    La version de votre API. À ne pas confondre avec la version OPENAPI. Elle apparaîtra dans la petite étiquette grise à côté de votre titre.

    Par défaut : ``0.1.0``


.. _JEROBOAM_DESCRIPTION:
.. py:data:: JEROBOAM_DESCRIPTION

    Une courte description de votre API. Elle apparaîtra dans la petite étiquette grise à côté de votre titre.

    Par défaut : ``None``


.. _JEROBOAM_TERMS_OF_SERVICE:
.. py:data:: JEROBOAM_TERMS_OF_SERVICE

        Un lien vers les conditions d'utilisation de votre API. Elle apparaîtra dans le pied de page de votre page de documentation OpenAPI.

        Par défaut : ``None``

.. _JEROBOAM_CONTACT:
.. py:data:: JEROBOAM_CONTACT

    Un dictionnaire contenant les informations de contact de votre API. Elle apparaîtra dans le pied de page de votre page de documentation OpenAPI.

    Par défaut : ``None``

.. _JEROBOAM_LICENCE_INFO:
.. py:data:: JEROBOAM_LICENCE_INFO

    Un dictionnaire contenant les informations de licence de votre API. Elle apparaîtra dans le pied de page de votre page de documentation OpenAPI.

    Par défaut : ``None``


.. _JEROBOAM_OPENAPI_VERSION:
.. py:data:: JEROBOAM_OPENAPI_VERSION

    La version de la spécification OpenAPI avec laquelle votre API est conforme. Elle apparaîtra dans le pied de page de votre page de documentation OpenAPI.

    Par défaut : ``3.0.2``


.. _JEROBOAM_SERVERS:
.. py:data:: JEROBOAM_SERVERS

    Une liste de dictionnaires contenant les serveurs sur lesquels votre API est disponible. Elle apparaîtra dans le pied de page de votre page de documentation OpenAPI.

    Par défaut : ``[]``


.. _JEROBOAM_OPENAPI_URL:
.. py:data:: JEROBOAM_OPENAPI_URL

    L'URL de votre page de documentation OpenAPI.

    Par défaut : ``/docs``

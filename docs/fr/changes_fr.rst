Modifications
=============

Version 0.2.0
-------------

Publiée le 10 mars 2026

**Changements cassants**

* **Pydantic v2 requis** — pydantic v1 n'est plus supporté. Mettez à jour votre environnement vers ``pydantic>=2.0`` avant de mettre à jour flask-jeroboam. Pydantic v2 continue de supporter les décorateurs ``@validator`` de style v1 avec un avertissement de dépréciation, donc la plupart du code de modèle fonctionnera sans changements.
* Le format de réponse d'erreur a été mis à jour pour correspondre aux conventions de pydantic v2 (par exemple ``"Field required"`` / ``"missing"`` au lieu de ``"field required"`` / ``"value_error.missing"``).

**Changements internes**

* Suppression complète du shim pydantic v1 ``_compat.py``
* ``ViewArgument`` hérite maintenant de ``FieldInfo`` pydantic v2
* ``SolvedArgument`` reconstruit autour de ``TypeAdapter`` — plus de dépendance à ``ModelField``
* La génération de schéma OpenAPI a été réécrite pour utiliser ``model_json_schema()`` et ``TypeAdapter.json_schema()``

versions bêta
*************

Les versions bêta marquent un tournant et l'intention de dépasser l'utilisation interne initiale de **Flask-Jeroboam**. La version 0.1.0 est principalement basée sur le forking de FastAPI et s'écarte de la première implémentation naïve des versions alpha.


Version 0.1.0.beta2
-------------------

Publiée le 9 mars 2023

* Rédaction de la documentation
* Correction de bogues
* Changement cassant : Correction du mécanisme d'incorporation pour les corps de requête

Version 0.1.0.beta
------------------

Publiée le 22 février 2023

* Support pour l'emplacement explicite des arguments entrants avec des fonctions spéciales
* Support pour les options de validation sur les arguments entrants explicites
* Le mécanisme de sérialisation des réponses a été amélioré
* Génération automatique de la documentation OpenAPI
* Vous pouvez ajouter des tags aux endpoints et aux blueprints
* Refactorisation extensive de la base de code

versions alpha
**************

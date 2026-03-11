# Alternatives et Comparaison

Flask-Jeroboam existe dans un espace avec plusieurs autres bibliothèques. Cette page vous donne une comparaison honnête pour que vous puissiez choisir le bon outil pour votre situation.

## Le paysage

| Bibliothèque   | Téléchargements mensuels | Approche                        | Pydantic       | Validation des réponses |
| -------------- | ----------------------- | ------------------------------- | -------------- | ----------------------- |
| flask-restx    | ~2,6M                   | Ressources basées sur les classes, Swagger UI | ❌ Aucun       | ❌                      |
| flask-smorest  | ~1,3M                   | Basée sur Marshmallow, OpenAPI  | ❌ Marshmallow | ❌                      |
| flask-openapi3 | ~2,2M                   | Injection de modèles nommés     | ✅ v2          | Optionnelle             |
| apiflask       | ~227K                   | Remplacement au niveau du cadre | Partielle      | ❌                      |
| spectree       | ~252K                   | Validation basée sur les décorateurs | ✅ v1+v2       | Optionnelle             |
| flask-jeroboam | —                       | Style FastAPI par paramètre     | ✅ v2          | ✅ Par défaut          |

---

## Flask-Jeroboam vs flask-openapi3

Flask-openapi3 est l'alternative fonctionnelle la plus proche et vaut la peine d'être comprise en profondeur avant de choisir entre elles.

### La différence de conception centrale

Les deux bibliothèques ont fait des paris opposés au cœur de leur API de déclaration de paramètres.

**flask-openapi3 utilise des noms d'arguments magiques réservés.** Vous groupez tous les paramètres d'un emplacement HTTP donné dans un seul modèle Pydantic, puis passez ce modèle comme argument de fonction dont le _nom_ indique à la bibliothèque où chercher :

```python
# flask-openapi3
class BookQuery(BaseModel):
    page: int = 1
    per_page: int = 10

class BookBody(BaseModel):
    title: str
    author: str

@app.post("/books")
def create_book(query: BookQuery, body: BookBody):
    # "query" et "body" sont des chaînes magiques — les noms déterminent la détection de localisation
    pass
```

**Flask-Jeroboam utilise des paramètres de fonction individuels**, avec la localisation déduite du contexte (verbe HTTP, motif de route) ou déclarée explicitement par paramètre — le même motif que FastAPI :

```python
# flask-jeroboam
@app.post("/books")
def create_book(page: int = 1, per_page: int = 10, title: str, author: str):
    # page, per_page → requête (déduit : paramètres de style GET)
    # title, author  → corps (déduit : défaut du verbe POST)
    # Pas de noms magiques, pas de modèles wrapper requis
    pass
```

Ce n'est pas juste du sucre syntaxique. Le choix architectural a des conséquences réelles.

---

### Où Flask-Jeroboam a un avantage structurel

#### 1. Composition des décorateurs et des middleware

Flask-openapi3 valide les requêtes en interceptant `**kwargs` au moment de l'appel et en traitant tout comme un argument de chemin. Cela casse tout décorateur qui injecte des arguments de mots-clés — décorateurs d'authentification, frameworks d'injection de dépendances, limiteurs de débit. Le résultat : les requêtes non authentifiées retournent `422 Validation Error` au lieu de `401 Unauthorized` car la validation s'exécute avant l'authentification ([problème flask-openapi3 #111](https://github.com/luolingchun/flask-openapi3/issues/111), [#143](https://github.com/luolingchun/flask-openapi3/issues/143)).

Flask-Jeroboam résout toutes les métadonnées des paramètres au **moment de l'enregistrement** (quand le décorateur s'exécute), pas au moment de la requête. La signature de la fonction de vue est inspectée une fois et un gestionnaire dédié est construit. Les décorateurs Flask standard se composent naturellement.

#### 2. Validation des réponses comme une fonctionnalité de première classe

Flask-openapi3 a été construit pour la génération de documentation ; la validation des réponses a été ajoutée plus tard en tant qu'option opt-in (`validate_response=True`). L'implémentation place un drapeau sur l'objet fonction, et le PR qui l'a ajouté a été immédiatement suivi d'un bug `AttributeError` ([#246](https://github.com/luolingchun/flask-openapi3/issues/246)).

Flask-Jeroboam a une validation bidirectionnelle dès le départ. Le `OutboundHandler` est un pair du `InboundHandler`, pas une pensée tardive. La validation des réponses est activée par défaut — si votre vue retourne des données qui ne correspondent pas au `response_model` déclaré, vous obtenez une `ResponseValidationError` en développement avant qu'elle n'atteigne un client.

#### 3. Pas de réimplémentation du schéma Pydantic

Flask-openapi3 réimplémente la traversée du schéma Pydantic en interne. C'est la cause profonde d'une classe récurrente de bogues : les propriétés `@computed_field` disparaissent de la documentation OpenAPI ([#139](https://github.com/luolingchun/flask-openapi3/issues/139)), les tuples se cassent après les mises à jour de version ([#183](https://github.com/luolingchun/flask-openapi3/issues/183)), les alias de champs cessent de fonctionner pour les données de formulaire ([#182](https://github.com/luolingchun/flask-openapi3/issues/182)), et les avertissements de dépréciation de `Field(example=...)` ([#176](https://github.com/luolingchun/flask-openapi3/issues/176), [#177](https://github.com/luolingchun/flask-openapi3/issues/177)).

Flask-Jeroboam délègue la génération de schéma à la propre fonction `model_json_schema()` de Pydantic plutôt que de la réimplémenter. Cette classe de bogue ne peut pas survenir par conception.

#### 4. Paramètres scalaires individuels sans modèles wrapper

Dans flask-openapi3, même un seul paramètre de requête nécessite d'être enrobé dans un `BaseModel` :

```python
# flask-openapi3 — vous avez besoin d'un modèle pour un seul paramètre
class PaginationQuery(BaseModel):
    page: int = 1

@app.get("/items")
def list_items(query: PaginationQuery):
    pass
```

Dans Flask-Jeroboam, les scalaires individuels fonctionnent directement :

```python
# flask-jeroboam — pas de wrapper nécessaire
@app.get("/items")
def list_items(page: int = 1):
    pass
```

#### 5. Valeurs par défaut intelligentes basées sur les verbes HTTP

Flask-Jeroboam déduit la localisation des paramètres du verbe HTTP — `GET`/`HEAD`/`DELETE` par défaut à la chaîne de requête ; `POST`/`PUT`/`PATCH` par défaut au corps de la requête. Cela supprime le besoin d'annoter la plupart des paramètres explicitement, tout en permettant les remplacements avec `Query()`, `Body()`, `Header()`, etc.

---

### Où flask-openapi3 a un avantage structurel

**Support de Pydantic v2.** Les deux bibliothèques supportent Pydantic v2 nativement. Flask-Jeroboam v0.2.0 a terminé une migration complète vers Pydantic v2 sans couche de compatibilité v1.

**Plus d'options d'interface utilisateur de documentation.** Flask-openapi3 supporte Swagger UI, ReDoc, RapiDoc, Scalar et Elements. Flask-Jeroboam fournit actuellement Swagger UI.

**Une plus grande base installée.** Plus d'utilisateurs signifie plus de tests en conditions réelles, plus de réponses Stack Overflow et plus de probabilité que votre question spécifique ait déjà été posée.

---

### Résumé

Choisissez **flask-openapi3** si :

- Vous préférez le groupement explicite des modèles à la place des déclarations par paramètre
- Vous avez besoin d'options d'interface utilisateur ReDoc, Scalar ou autres au-delà de Swagger

Choisissez **Flask-Jeroboam** si :

- Vous êtes familiarisé avec FastAPI et voulez cette syntaxe exacte de paramètres
- Vous avez besoin de la validation des réponses activée par défaut, pas optionnelle
- Vous avez besoin d'une composition claire des décorateurs/middleware sans surprises d'ordre de validation
- Vous voulez que la génération du schéma Pydantic soit déléguée à Pydantic lui-même, pas réimplémentée

---

## Flask-Jeroboam vs FastAPI

FastAPI n'est pas une extension Flask — c'est un framework séparé construit sur Starlette/ASGI. Flask-Jeroboam est explicitement modélisé d'après la syntaxe des paramètres de FastAPI, donc la plupart des motifs FastAPI se transfèrent directement.

Choisissez **FastAPI** si :

- Vous démarrez un nouveau projet sans héritage Flask
- Vous avez besoin d'async/await natif partout
- Les performances d'ASGI sont une exigence

Choisissez **Flask-Jeroboam** si :

- Vous avez une base de code Flask existante
- Vous dépendez d'extensions spécifiques à Flask (Flask-Login, Flask-Admin, Flask-SQLAlchemy, etc.)
- Vous utilisez le rendu côté serveur aux côtés de votre API
- Vous avez besoin d'un déploiement WSGI

---

## Flask-Jeroboam vs flask-smorest / flask-restx

Ces bibliothèques sont basées sur marshmallow (flask-smorest) ou pré-indices de type dans la conception (flask-restx). Si votre équipe utilise déjà Pydantic pour la modélisation des données, l'inadéquation d'impédance avec les schémas marshmallow ajoute un surcoût réel. Flask-Jeroboam vous permet d'utiliser les mêmes modèles Pydantic pour la couche de base de données, la logique métier et la validation API sans traduction.

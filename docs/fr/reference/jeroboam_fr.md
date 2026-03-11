# Jeroboam

La classe d'application principale.

## Jeroboam

```python
class Jeroboam(Flask)
```

Une sous-classe Flask qui ajoute l'analyse des requêtes, la validation des réponses et la documentation OpenAPI.

### Constructeur

```python
Jeroboam(*args, **kwargs)
```

Prend les mêmes paramètres que `Flask`. Voir la [documentation Flask](https://flask.palletsprojects.com/en/stable/api/#flask.Flask) pour plus de détails.

À l'initialisation, Jeroboam charge sa configuration depuis `JeroboamConfig` (qui lit les variables d'environnement) et la fusionne dans `app.config`. Les paramètres spécifiques à Jeroboam se configurent via `app.config` après la construction :

- `JEROBOAM_REGISTER_OPENAPI` (bool) : Enregistrer les endpoints OpenAPI. Défaut : `True`
- `JEROBOAM_REGISTER_ERROR_HANDLERS` (bool) : Enregistrer les gestionnaires d'erreurs de validation. Défaut : `True`
- `JEROBOAM_OPENAPI_URL` (str) : Chemin vers la documentation interactive. Défaut : `/docs`
- `JEROBOAM_TITLE` (str) : Titre de l'API dans le schéma OpenAPI. Défaut : `None`
- `JEROBOAM_VERSION` (str) : Version de l'API. Défaut : `0.1.0`
- `JEROBOAM_DESCRIPTION` (str) : Description de l'API. Défaut : `None`

### Méthodes

#### route

```python
def route(
    rule: str,
    **options
) -> Callable
```

Enregistre une fonction de vue pour une règle d'URL donnée. Fonctionne comme le décorateur `route()` de Flask mais ajoute la validation requête/réponse.

**Exemple :**

```python
@app.route("/items", methods=["GET"])
def list_items():
    return [{"id": 1, "name": "Item 1"}]
```

#### get, post, put, patch, delete, options, head

```python
def get(rule: str, **options) -> Callable
def post(rule: str, **options) -> Callable
def put(rule: str, **options) -> Callable
def patch(rule: str, **options) -> Callable
def delete(rule: str, **options) -> Callable
def options(rule: str, **options) -> Callable
def head(rule: str, **options) -> Callable
```

Raccourcis pour les méthodes HTTP. Chacun fonctionne comme les décorateurs de méthode de Flask mais avec validation.

**Exemple :**

```python
@app.get("/wines/<int:wine_id>")
def get_wine(wine_id: int):
    return {"id": wine_id}

@app.post("/wines")
def create_wine(name: str, vintage: int):
    return {"name": name, "vintage": vintage}
```

#### add_url_rule

```python
def add_url_rule(
    rule: str,
    endpoint: str = None,
    view_func: Callable = None,
    **options
) -> None
```

Enregistre une règle d'URL avec une fonction de vue. Fonctionne comme la méthode `add_url_rule()` de Flask.

### Propriétés

#### jeroboam_config

```python
@property
def jeroboam_config(self) -> dict
```

Retourne la configuration spécifique à Jeroboam.

---

## Blueprint

```python
class Blueprint(Flask.Blueprint)
```

Une sous-classe de Blueprint qui ajoute l'analyse des requêtes et la validation des réponses.

Fonctionne exactement comme Jeroboam mais pour organiser les routes en modules. Utilisez `blueprint.route()`, `blueprint.get()`, etc. de la même façon que Jeroboam.

**Exemple :**

```python
from flask_jeroboam import Blueprint

wines_bp = Blueprint("wines", __name__)

@wines_bp.get("/wines")
def list_wines():
    return []

app.register_blueprint(wines_bp)
```

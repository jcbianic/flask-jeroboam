# Jeroboam

La classe d'application principale.

## Jeroboam

```python
class Jeroboam(Flask)
```

Une sous-classe Flask qui ajoute l'analyse des requêtes, la validation des réponses et la documentation OpenAPI.

### Constructeur

```python
Jeroboam(
    import_name: str,
    static_url_path: str = "/static",
    static_folder: str = "static",
    static_host: str = None,
    host_matching: bool = False,
    subdomain_matching: bool = False,
    template_folder: str = "templates",
    instance_path: str = None,
    instance_relative_config: bool = False,
    root_path: str = None,
    openapi_enabled: bool = True,
    openapi_url_prefix: str = "/",
    docs_url: str = "/docs"
)
```

**Paramètres :**

- `import_name` (str) : Le nom du module pour l'application
- `openapi_enabled` (bool) : Si les documents OpenAPI doivent être générés. Défaut : `True`
- `openapi_url_prefix` (str) : Préfixe d'URL pour les endpoints OpenAPI. Défaut : `/`
- `docs_url` (str) : Chemin vers la documentation interactive. Défaut : `/docs`

Tous les autres paramètres sont hérités de Flask.

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

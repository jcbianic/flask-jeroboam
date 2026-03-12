# Gestion des erreurs

Réponses d'erreur et exceptions de validation.

## Erreurs de validation

Quand la validation de la requête échoue, Jeroboam retourne une réponse 422 Unprocessable Entity avec des détails sur ce qui a échoué.

### Format

```json
{
  "detail": [
    {
      "loc": ["query", "page"],
      "msg": "Input should be a valid integer",
      "type": "int_parsing"
    }
  ]
}
```

**Champs :**

- `loc` (tableau) : Localisation de l'erreur (par ex. `["query", "field_name"]`)
- `msg` (chaîne) : Message d'erreur lisible par l'homme
- `type` (chaîne) : Code de type d'erreur (par ex. `"int_parsing"`, `"string_type"`, `"value_error"`)

### Types d'erreurs courants

- `"int_parsing"` - Attendu un entier
- `"float_parsing"` - Attendu un décimal
- `"string_type"` - Attendu une chaîne
- `"bool_parsing"` - Attendu un booléen
- `"list_type"` - Attendu une liste
- `"dict_type"` - Attendu un dict
- `"value_error"` - La valeur viole les contraintes (par ex. `gt=0`)
- `"greater_than"` - La valeur n'est pas plus grande que le minimum
- `"less_than"` - La valeur n'est pas moins que le maximum
- `"string_too_short"` - La chaîne est plus courte que `min_length`
- `"string_too_long"` - La chaîne est plus longue que `max_length`
- `"string_pattern_mismatch"` - La chaîne ne correspond pas au `pattern`
- `"missing"` - Le champ requis manque

---

## Erreurs de validation de réponse

Quand la validation de réponse échoue (seulement en développement), Jeroboam lève une erreur avant d'envoyer la réponse.

**Exemple d'erreur :**

```
ValidationError: 1 validation error for WineOut
vintage
  Field required (type=missing)
```

Cela indique que votre fonction a retourné des données manquant le champ `vintage`.

---

## Gestionnaires d'erreurs personnalisés

Utilisez `@app.errorhandler` de Flask pour personnaliser les réponses d'erreur.

```python
from werkzeug.exceptions import HTTPException

@app.errorhandler(422)
def handle_validation_error(e):
    return {
        "error": "Validation failed",
        "details": e.description
    }, 422
```

---

## Lever des erreurs de validation

Pour la validation personnalisée dans vos fonctions :

```python
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

@app.post("/items")
def create_item(item: Item):
    if item.price < 0:
        raise BadRequest("Price cannot be negative")
    return item
```

---

## Exceptions HTTP

Les exceptions HTTP standard de Flask fonctionnent normalement.

```python
from werkzeug.exceptions import NotFound, Forbidden

@app.get("/items/<int:item_id>")
def get_item(item_id: int):
    if item_id < 0:
        raise NotFound("Item not found")
    return {"id": item_id}
```

Celles-ci retournent les codes de statut HTTP appropriés (404, 403, etc.) sans déclencher le formatage d'erreur de validation de Jeroboam.

---

## Documentation des erreurs OpenAPI

Documentez les réponses d'erreur dans OpenAPI avec des descriptions d'erreur personnalisées.

```python
@app.get(
    "/items",
    responses={
        404: {"description": "Item not found"},
        500: {"description": "Server error"}
    }
)
def get_item():
    return {}
```

Cela ajoute des réponses d'erreur à la documentation `/docs`.

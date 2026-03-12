# Configuration de réponse

Décorateurs et paramètres pour la gestion des réponses.

## response_model

```python
response_model: Type[BaseModel] = None
```

Déclare le modèle de réponse pour une route. Valide et sérialise les réponses.

**Exemple :**

```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    name: str
    price: float

@app.get("/items", response_model=List[Item])
def list_items():
    return [
        {"id": 1, "name": "Item 1", "price": 9.99},
        {"id": 2, "name": "Item 2", "price": 19.99}
    ]
```

---

## status_code

```python
status_code: int = None
```

Définit le code de statut HTTP pour les réponses réussies.

**Exemple :**

```python
@app.post("/items", status_code=201)
def create_item(item: Item):
    return item
```

---

## response_description

```python
response_description: str = None
```

Définit la description de la réponse dans la documentation OpenAPI.

**Exemple :**

```python
@app.get("/items", response_description="List of all items")
def list_items():
    return []
```

---

## validate_response

```python
validate_response: bool = True
```

Active ou désactive la validation des réponses. La valeur par défaut est `True`.

**Exemple :**

```python
@app.get("/fast", validate_response=False)
def fast_endpoint():
    # La réponse n'est pas validée
    return {"data": "..."}
```

Désactivez ceci uniquement si vous êtes sûr de la correction des réponses et que vous avez besoin de ignorer la surcharge de validation.

---

## Configuration de sérialisation de réponse

Utilisez la configuration du modèle Pydantic pour contrôler la sérialisation.

### by_alias

```python
class Item(BaseModel):
    internal_id: int = Field(alias="id")

    model_config = ConfigDict(by_alias=True)
```

Sérialise les champs en utilisant leurs alias.

### exclude_none

```python
class Item(BaseModel):
    name: str
    description: str = None

    model_config = ConfigDict(exclude_none=True)
```

Exclut les champs avec des valeurs `None` de la réponse.

### exclude_unset

```python
class Item(BaseModel):
    name: str
    description: str = "Default"

    model_config = ConfigDict(exclude_unset=True)
```

Exclut les champs qui n'ont pas été explicitement définis.

---

## Sérialisation de champs

Contrôlez comment les champs individuels se sérialisent.

### alias

```python
from pydantic import Field

class Item(BaseModel):
    internal_id: int = Field(alias="id")
```

Utilise un nom différent dans la réponse JSON.

### serialization_alias

```python
from pydantic import Field

class Item(BaseModel):
    internal_id: int = Field(
        validation_alias="internalId",
        serialization_alias="id"
    )
```

Utilise des noms différents pour la validation et la sérialisation.

### field_serializer

```python
from pydantic import field_serializer

class Item(BaseModel):
    price: float

    @field_serializer('price')
    def serialize_price(self, value: float) -> str:
        return f"${value:.2f}"
```

Logique de sérialisation personnalisée pour un champ.

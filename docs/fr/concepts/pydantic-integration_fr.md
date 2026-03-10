# Pourquoi et comment nous utilisons Pydantic

Pydantic est l'épine dorsale de Flask-Jeroboam. Comprendre comment nous l'utilisons aide à expliquer les choix de conception et ce qui est possible.

## Ce que Pydantic fait

Pydantic valide les objets Python par rapport à un schéma. Vous définissez un modèle avec des champs et des types :

```python
from pydantic import BaseModel

class Wine(BaseModel):
    name: str
    vintage: int
    region: str = "Unknown"
```

Puis vous validez les données :

```python
wine = Wine(**{"name": "Château Lafite", "vintage": "2015"})
# Pydantic contraint "2015" à 2015
# wine.vintage est maintenant un int
```

Si les données sont invalides, Pydantic lève une erreur avec des détails sur ce qui a échoué.

C'est l'insight principal : Pydantic transforme la validation en un problème déclaratif. Vous décrivez ce que vous voulez (indices de type), et Pydantic l'applique.

## Pourquoi cela importe pour la validation des requêtes

Flask vous donne les données brutes des requêtes comme des chaînes et des dicts :

```python
# request.args est {"page": "1", "limit": "10"}
# request.get_json() est {"name": "Château Lafite", "vintage": "2015"}
```

Tout est une chaîne ou un dict imbriqué. Pas de types. Pas de validation.

Votre signature de fonction dit ce que vous avez besoin :

```python
def list_wines(page: int = 1, limit: int = 10):
    ...
```

Jeroboam comble ce fossé. Il utilise Pydantic pour :
1. Construire un modèle de validation à partir de votre signature de fonction
2. Extraire et valider les données de la requête
3. Transmettre les arguments validés à votre fonction

Vous n'écrivez pas de code de validation. Pydantic gère le mappage.

## Pourquoi TypeAdapter

Dans Pydantic v2, `TypeAdapter` est l'outil pour valider des types arbitraires sans BaseModel :

```python
from pydantic import TypeAdapter

adapter = TypeAdapter(int)
result = adapter.validate_python("42")  # 42
```

Jeroboam utilise TypeAdapter pour chaque paramètre. Pourquoi ? Parce que les paramètres de fonction peuvent être n'importe quoi :

```python
def get_user(user_id: int):
    # Type simple
    ...

def search(tags: List[str] = Query(...)):
    # Type complexe
    ...

def process(config: Dict[str, Any] = Body(...)):
    # Dict imbriqué
    ...
```

BaseModel ne fonctionne que pour les classes. TypeAdapter fonctionne pour n'importe quel type : scalaires, listes, unions, classes personnalisées. C'est la flexibilité que Jeroboam fournit.

## Pourquoi FieldInfo

Le `FieldInfo` de Pydantic v2 est l'objet métadonnées qui décrit les contraintes sur un champ :

```python
from pydantic import Field

page: int = Field(1, ge=1, le=100)
```

Cet appel `Field(...)` retourne un objet `FieldInfo` avec des informations sur les valeurs par défaut, les contraintes, les descriptions, les alias, etc.

Le `Query`, `Body`, `Header`, etc. de Jeroboam sont des sous-classes de `FieldInfo`. Quand vous écrivez :

```python
page: int = Query(1, ge=1)
```

Vous fournissez des métadonnées Pydantic qui décrivent ce paramètre. Jeroboam lit ces métadonnées et construit les règles de validation à partir de celles-ci.

L'avantage : vous utilisez le système de contrainte de Pydantic directement. `Field(ge=1, le=100)` signifie « supérieur ou égal à 1, inférieur ou égal à 100 ». La même syntaxe fonctionne dans les modèles de réponse, les paramètres du corps, les paramètres de requête : partout.

## Validation à l'heure d'enregistrement vs. l'heure de requête

C'est là que la conception devient intéressante. Jeroboam fait le travail de validation à deux moments :

### Heure d'enregistrement (quand vous décorez la fonction)

```python
@app.get("/wines")
def list_wines(page: int = 1):
    ...
```

Jeroboam inspecte votre signature immédiatement. Il :
- Lit l'indice de type (`int`)
- Lit toutes les métadonnées (`Field(...)`, `Query(...)`, etc.)
- Construit un `TypeAdapter` Pydantic pour ce paramètre
- Le stocke dans un `SolvedArgument` (un plan de validation pré-construit)

C'est du travail coûteux, mais cela se produit une fois.

### Heure de requête (quand une requête arrive)

La requête arrive. Jeroboam :
1. Extrait le paramètre de la source appropriée (requête, corps, en-têtes)
2. Exécute le TypeAdapter pré-construit
3. Transmet la valeur validée à votre fonction

C'est rapide parce que le gros du travail est fait.

L'insight : validez une fois à l'enregistrement, utilisez plusieurs fois à l'heure de requête.

## Comment Pydantic gère les corps de requête

Quand vous acceptez un modèle Pydantic dans votre requête :

```python
class WineCreate(BaseModel):
    name: str
    price: float

@app.post("/wines")
def create_wine(wine: WineCreate):
    ...
```

Jeroboam ne transmet pas le JSON brut de la requête à votre fonction. Il :
1. Extrait le corps JSON
2. Le transmet à `WineCreate.model_validate(data)` de Pydantic
3. Pydantic valide et retourne une instance `WineCreate`
4. Transmet cette instance à votre fonction

Votre fonction reçoit un objet entièrement validé avec des propriétés comme `wine.name` et `wine.price`.

## Comment Pydantic gère plusieurs paramètres

Vous pouvez mélanger des paramètres simples avec des modèles Pydantic :

```python
@app.post("/wines")
def create_wine(
    wine: WineCreate,
    skip_notification: bool = Query(False)
):
    ...
```

Jeroboam construit un modèle Pydantic temporaire qui a à la fois `wine` (un modèle WineCreate imbriqué) et `skip_notification` (un booléen de la chaîne de requête). Puis il agrège les données des deux sources et valide tout ensemble.

C'est pourquoi Jeroboam peut gérer des scénarios complexes sans code personnalisé.

## Validation de réponse avec Pydantic

Sur le chemin du retour, votre fonction retourne des données. Jeroboam les valide :

```python
class WineOut(BaseModel):
    name: str
    vintage: int

@app.get("/wines/<int:wine_id>", response_model=WineOut)
def get_wine(wine_id: int):
    return {"name": "Château Lafite", "vintage": 2015}
```

Jeroboam appelle `WineOut.model_validate(response_data)`. Si la validation échoue, elle lève une erreur (en mode développement, bruyamment).

Ceci attrape les bogues où votre fonction retourne des données qui ne correspondent pas au schéma. En production, vous pouvez l'éteindre si vous êtes confiant (bien que nous ne le recommandions pas).

## Alias de sérialisation

Les modèles Pydantic peuvent avoir des noms de champs différents dans Python vs. JSON :

```python
class WineOut(BaseModel):
    name: str
    total_reviews: int = Field(alias="totalReviews")

    model_config = ConfigDict(
        alias_generator=to_camel_case,
        ser_by_alias=True
    )
```

Votre fonction fonctionne avec `wine.total_reviews`. Les réponses JSON utilisent `totalReviews`. Pydantic gère le mappage automatiquement.

## Validateurs personnalisés

Pydantic supporte la logique de validation personnalisée :

```python
class EventCreate(BaseModel):
    start_date: date
    end_date: date

    @field_validator('end_date')
    @classmethod
    def end_after_start(cls, v, info):
        if v <= info.data.get('start_date'):
            raise ValueError('end_date doit être après start_date')
        return v
```

Jeroboam exécute ces validateurs. Validation inter-champs, validation conditionnelle, n'importe quoi que Pydantic supporte.

## Champs calculés

Pydantic peut générer des champs à partir d'autres champs :

```python
class Person(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

Lors de la sérialisation en JSON, `full_name` apparaît dans la sortie sans être un champ stocké. Jeroboam le respecte dans les modèles de réponse.

## Le coût

La validation Pydantic a une surcharge. Pour les endpoints simples avec quelques paramètres, c'est négligeable. Pour les APIs à haut débit, vous le remarquez.

Jeroboam atténue cela en faisant une validation d'enregistrement une fois, pas par requête. Mais le coût est toujours là.

Si vous avez besoin d'une performance extrême sur un endpoint spécifique, vous pouvez désactiver la validation de réponse :

```python
@app.get("/fast", validate_response=False)
def fast_endpoint():
    ...
```

Vous perdez la sécurité, mais gagnez la vitesse.

## Pourquoi pas une autre bibliothèque de validation

Certaines alternatives :

- **Marshmallow** : Plus lourd, plus lent, motifs matures mais plus anciens
- **Cerberus** : Plus simple mais moins puissant
- **Logique personnalisée regex/** : Sujette aux erreurs, difficile à maintenir

Pydantic est rapide, complet, et est devenu la norme dans les frameworks web Python modernes. L'utiliser signifie :
- La plupart des développeurs en sont familiers
- La documentation et les exemples existent
- La performance est bonne
- L'intégration avec d'autres outils (SQLAlchemy, dataclasses) est transparente

## La migration v2

Jeroboam a été construit sur Pydantic v1. Pydantic v2 a changé considérablement : plus rapide, validation plus précise, meilleure gestion des types.

Jeroboam v0.2.0 cible Pydantic v2. Cela impliquait :
- Mise à jour des validateurs (`@validator` → `@field_validator`)
- Utilisation de TypeAdapter au lieu de wrappers de validation personnalisés
- Adoption des motifs FieldInfo de v2

L'avantage : Jeroboam utilise maintenant Pydantic moderne. Le coût : si vous êtes sur Pydantic v1, vous devez mettre à niveau.

## Conclusion

Pydantic n'est pas une exigence pour utiliser Flask. Vous pouvez utiliser Flask sans lui. Mais Jeroboam l'exige parce que Pydantic valide si bien. Plutôt que de réinventer la validation, nous avons intégré avec l'outil qui le fait mieux.

Si vous avez utilisé Pydantic ailleurs (FastAPI, SQLModel, de nombreux frameworks web), l'utilisation de Pydantic par Jeroboam vous semblera naturelle.

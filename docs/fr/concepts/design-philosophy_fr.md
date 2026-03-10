# Philosophie de conception

Flask-Jeroboam existe parce que nous avons cru que Flask avait besoin d'une meilleure façon de gérer la validation des requêtes et la sérialisation des réponses sans abandonner la simplicité de Flask.

## Le problème que nous avons résolu

Flask vous donne les données brutes des requêtes. Vous écrivez du code pour les valider, les transformer, les contraindre à des types, gérer les erreurs. La même danse, répétée à chaque endpoint. Les développeurs ignorent soit la validation (« c'est juste pour mon API interne »), la réinventent par projet, ou superposent un framework comme FastAPI.

Mais passer à FastAPI signifie quitter l'écosystème Flask. Vous perdez les extensions Flask, les motifs d'intergiciels, le code existant. Partir de zéro est cher.

Jeroboam a demandé : et si vous pouviez avoir la flexibilité de Flask avec la validation automatique intégrée ? Pas comme un remplacement de framework, mais comme une extension naturelle de Flask lui-même.

## Pourquoi les indices de type, pas les schémas

Beaucoup de frameworks (marshmallow, jsonschema) séparent votre schéma de votre code :

```python
# Schéma défini séparément
schema = ItemSchema()

# La fonction ne le sait rien
def create_item(data):
    item = schema.load(data)
    ...
```

Jeroboam rend votre signature de fonction le schéma :

```python
def create_item(name: str, price: float = Field(..., gt=0)):
    ...
```

Pourquoi ? Votre signature décrit déjà ce que vous attendez. La rendre la source de vérité signifie :

- Aucune duplication (un seul endroit à mettre à jour quand les exigences changent)
- Support IDE (votre éditeur comprend les types)
- Documentation (la signature est auto-documentée)
- Moins de passe-partout (une annotation au lieu de définitions de champs dans deux endroits)

C'est la même philosophie que FastAPI utilise. Jeroboam l'apporte à Flask.

## Pourquoi Pydantic

Pydantic valide bien. Il gère la coercition de type, les modèles imbriqués, les unions discriminantes, les champs calculés, les validateurs personnalisés — des dizaines de cas limites que nous ne voulons pas réinventer.

Pydantic v2 est rapide et a de bons messages d'erreur. Plutôt que de construire une autre bibliothèque de validation, nous avons intégré Pydantic comme moteur de validation principal.

C'est un compromis délibéré. Jeroboam apporte Pydantic comme une dépendance stricte. Si vous l'utilisez déjà (et la plupart des projets Flask modernes le font), vous obtenez Jeroboam gratuitement. Si vous ne l'êtes pas, vous prenez une dépendance.

## Pourquoi la documentation automatique

Les spécifications OpenAPI sont utiles mais ennuyeuses à maintenir. Les équipes écrivent des spécifications, puis le code s'en éloigne. Ou la spécification n'est jamais mise à jour.

Jeroboam génère OpenAPI à partir de votre code. Renommez un paramètre, mettez à jour la documentation. Ajoutez une contrainte, la documentation la montre. La documentation ne peut pas être périmée parce qu'elle est générée à partir de ce qui fonctionne réellement.

C'est automatique, pas optionnel. Chaque app Jeroboam obtient la documentation à `/docs` par défaut. Pas parce que nous aimons OpenAPI, mais parce que la documentation générée qui reste synchronisée est plus précieuse que la documentation manuelle qui devient obsolète.

## Comparé aux alternatives

### FastAPI

FastAPI fait ce que Jeroboam fait mais comme un framework complet. Avantages : solution complète, excellente documentation, grand écosystème. Inconvénients : si vous voulez rester sur Flask, vous êtes en dehors de la chance. FastAPI n'est pas une couche Flask : c'est un remplacement.

Jeroboam est pour les équipes qui ont choisi Flask et veulent sa flexibilité mais aussi la validation et la documentation.

### flask-openapi3

Positionnement très similaire à Jeroboam. Apporte aussi les indices de type et OpenAPI automatique à Flask. La différence principale : nous avons opté pour les modèles Pydantic comme interface principale, tandis que flask-openapi3 utilise les schémas basés sur OpenAPI.

Les deux sont des choix solides. La différence est philosophique : voulez-vous que votre code soit centré sur Pydantic ou sur OpenAPI ?

### flask-restx

Plus ancien, basé sur marshmallow. Vues basées sur des classes et décorateurs. Toujours populaire, mais plus lourd et moins aligné avec les pratiques Python modernes (indices de type, dataclasses, Pydantic).

### Marshmallow

Éprouvé et très utilisé. Mais séparé de la signature de votre fonction, et nécessite des définitions de schéma manuelles.

## Ce que nous n'avons pas fait

### Pas de décorateurs magiques sur les paramètres

Certains frameworks nécessitent des décorateurs sur tous les paramètres :

```python
def get_wines(
    page: int = Query(...),
    vintage: int = Query(...)
):
    ...
```

Jeroboam rend les décorateurs optionnels. Les paramètres non décorés suivent des valeurs par défaut sensibles :
- Requêtes GET : paramètres de requête
- POST/PUT : champs du corps
- Paramètres de chemin : auto-détectés de l'URL

Vous pouvez utiliser des décorateurs pour la clarté ou pour contourner les valeurs par défaut, mais vous n'en avez pas besoin pour les cas simples.

### Pas de langage de sérialisation personnalisé

Certains frameworks inventent une syntaxe de sérialisation personnalisée. Jeroboam utilise les sérialiseurs de champ de Pydantic, qui sont juste des méthodes Python :

```python
class WineOut(BaseModel):
    name: str
    vintage: int

    @field_serializer('vintage')
    def serialize_vintage(self, value):
        return f"Year {value}"
```

C'est Python, pas un DSL. Si vous connaissez Python, vous pouvez le lire et l'écrire.

### Pas d'abandon des conventions Flask

Jeroboam est une app Flask. Vous utilisez `@app.get()`, `request`, `g`, intergiciels Flask, tout normal Flask. Rien de propriétaire.

Cela signifie :
- Les extensions Flask fonctionnent
- Vos connaissances Flask se transfèrent
- Migrer vers ou depuis Jeroboam est une refonte, pas une réécriture

## Les compromis

Jeroboam échange la simplicité dans certains domaines pour la clarté dans d'autres.

**Nous avons ajouté :** Pydantic comme dépendance (petite, rapide, largement utilisée)

**Nous avons retiré :** Code de validation manuelle dans la plupart des fonctions

**Nous avons rendu implicite :** Mappage type-vers-localisation (les paramètres GET sont des requêtes, les paramètres POST sont le corps)

**Nous avons rendu explicite :** Quand vous devez contourner (utiliser `Query()`, `Body()`, etc.)

## Direction future

Jeroboam vise à rester concentré. Nous ne essayons pas d'être un framework complet. Nous essayons d'être la meilleure façon d'ajouter la validation et la documentation à Flask sans changer Flask lui-même.

Où nous pourrions aller :
- Meilleur support async (l'histoire de Flask ici évolue toujours)
- Support des réponses en continu
- Génération de schéma GraphQL (peut-être)

Où nous n'irons pas :
- Authentification/autorisation (les extensions Flask comme Flask-Login existent)
- Intégration de base de données (utiliser SQLAlchemy, Alembic : Flask est agnostique au framework)
- Caractéristiques complètes du framework (routage, intergiciel, templating : Flask le fait)

Jeroboam est une couche sur Flask, pas un remplacement de Flask.

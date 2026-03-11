# Comment Flask-Jeroboam fonctionne en interne

Flask-Jeroboam s'intercale entre votre fonction de vue et le cycle requête/réponse de Flask. Quand vous décorez une fonction avec `@app.get()`, Jeroboam l'enveloppe avec une logique qui inspecte votre signature de fonction, extrait les données de la requête, les valide selon vos indices de type, puis valide la réponse avant qu'elle ne quitte.

## Les trois étapes de la gestion des requêtes

### 1. Temps d'enregistrement (Quand le décorateur s'exécute)

Quand vous écrivez :

```python
@app.get("/wines/<int:wine_id>")
def get_wine(wine_id: int, include_notes: bool = False):
    ...
```

Le `InboundHandler` de Jeroboam s'exécute immédiatement. Il inspecte la signature de votre fonction et construit un plan pour gérer les requêtes. C'est là que se fait le gros du travail : il figure que `wine_id` provient de l'URL, que `include_notes` provient des paramètres de requête, les types qu'ils doivent être, et les validations qui s'appliquent.

Point clé : nous faisons une introspection coûteuse une fois à l'enregistrement, pas à chaque requête.

### 2. Temps de requête (Quand une requête arrive)

Un client frappe votre endpoint. Flask le route, puis le `JeroboamView` de Jeroboam intercepte avant que votre fonction ne s'exécute. Il :

1. Extrait les données de la requête (paramètres de chemin, chaîne de requête, corps, en-têtes, cookies)
2. Les transmet par le plan de validation construit à l'enregistrement
3. Appelle votre fonction avec des arguments validés
4. Attrape la valeur de retour pour valider la réponse

Votre fonction voit des arguments propres et validés. Aucun code défensif nécessaire. Si la requête est invalide, Jeroboam retourne une erreur 422 avant que votre code ne s'exécute.

### 3. Temps de réponse (Après que votre fonction retourne)

Votre fonction retourne des données. Jeroboam les valide par rapport à votre modèle de réponse, les sérialise en JSON, et les renvoie. Si votre fonction retourne un vin manquant un champ, Jeroboam attrape cela en développement et échoue bruyamment.

C'est un filet de sécurité : en production, les réponses mal configurées sont détectées rapidement.

## À l'intérieur du validateur de requête

Voici ce qui se passe en détail quand une requête arrive.

### Rassembler les données

Flask a déjà analysé l'URL et extrait les paramètres de chemin. Jeroboam ajoute :

- Paramètres de requête (de `request.args`)
- Corps de la requête (de `request.get_json()`, en utilisant la validation de modèle de Pydantic)
- En-têtes (de `request.headers`)
- Cookies (de `request.cookies`)
- Paramètres de chemin (déjà analysés par Flask)

Chaque source de données est maintenue séparée : le plan construit à l'enregistrement sait quel paramètre provient d'où.

### L'étape de validation

C'est ici que Pydantic entre. Jeroboam construit un modèle Pydantic temporaire qui a un champ pour chacun de vos paramètres de fonction. Pour chaque source (requête, corps, en-têtes), il crée un modèle Pydantic et valide les données entrantes.

Pourquoi cette approche ? Pydantic est rapide, complet, et gère des centaines de cas limites que nous ne voulons pas réinventer. Nous l'exploitons complètement.

### Adaptation de type

Chaque paramètre est enveloppé dans un `TypeAdapter` : l'outil de Pydantic pour valider des types arbitraires, pas seulement des sous-classes de BaseModel. Cela signifie que vous pouvez accepter des listes, des unions, des chaînes littérales, n'importe quoi. Pydantic le gère.

## Comment les réponses sont validées

Quand vous spécifiez un `response_model`, Jeroboam ne laisse rien passer.

```python
class WineOut(BaseModel):
    name: str
    vintage: int
    region: str = "Unknown"

@app.get("/wines/<int:wine_id>", response_model=WineOut)
def get_wine(wine_id: int):
    return {"name": "Château Lafite", "vintage": 2015}  # Manque region !
```

Votre fonction retourne un dict manquant `region`. En mode développement, Jeroboam lève une erreur. Vous le voyez immédiatement. En production, la validation de réponse est toujours active par défaut, les endpoints mal configurés échouent donc en toute sécurité.

Vous pouvez aussi retourner une liste, des structures imbriquées, ou n'importe quel type que votre annotation supporte :

```python
@app.get("/wines", response_model=List[WineOut])
def list_wines():
    ...
```

La validation de liste utilise le `TypeAdapter` de Pydantic pour gérer le conteneur et chaque élément.

## Le plan d'enregistrement

À l'heure du décorateur, Jeroboam construit un `SolvedArgument` pour chaque paramètre. Cela contient :

- D'où provient le paramètre (requête, corps, chemin, en-tête, cookie)
- Le type attendu et toutes les contraintes de validation
- Un `TypeAdapter` Pydantic prêt à valider les données
- Les métadonnées de sérialisation (alias de champ, exclusions de champ, etc.)

Ceci est précalculé. À chaque requête, Jeroboam exécute simplement les validateurs déjà construits. Aucune introspection de signature à chaque requête.

## Pourquoi cela importe

La séparation du temps d'enregistrement du temps de requête donne à Jeroboam plusieurs propriétés :

**Vitesse** : L'introspection coûteuse se produit une fois. Les requêtes sont rapides.

**Clarté** : Votre signature de fonction est la source de vérité. Aucun fichier de schéma séparé, aucun décorateur sur les paramètres de fonction (sauf si vous le voulez). Jeroboam lit vos types et construit tout le reste.

**Sécurité** : Les requêtes invalides sont rejetées avant que votre code ne s'exécute. Les réponses sont vérifiées. Les mauvaises données ne atteignent pas silencieusement votre logique métier.

**Débogage** : Les messages d'erreur sont précis parce que Pydantic vous dit exactement ce qui a échoué et pourquoi. Pas « mauvaise requête », mais « le champ 'vintage' devrait être un entier, j'ai obtenu 'abc' ».

## Intégration avec Flask

Jeroboam est une sous-classe de Flask et Blueprint. Quand vous utilisez `Jeroboam(__name__)` au lieu de `Flask(__name__)`, vous obtenez le même objet Flask avec l'analyse des requêtes et la validation des réponses en couche supérieure.

Cela signifie :

- Compatible avec les intergiciels Flask
- Fonctionne avec les extensions Flask
- Les mêmes objets `request` et `g`
- Les décorateurs comme `@app.before_request` fonctionnent comme prévu

L'enveloppe se produit au niveau de la vue : le routage, les intergiciels et la gestion des erreurs de Flask ne sont pas modifiés.

## Génération OpenAPI

Jeroboam génère automatiquement des spécifications OpenAPI et sert la documentation interactive à `/docs`. Comment ? En lisant les informations qu'il a déjà rassemblées à l'heure d'enregistrement.

Votre signature de fonction + indices de type + modèle de réponse + docstring + toutes les descriptions de paramètres explicites = tout ce qui est nécessaire pour OpenAPI. Aucune définition de schéma séparée, aucune duplication.

L'endpoint `/docs` reflète votre API réelle. Renommez un paramètre, et la documentation se met à jour. Ajoutez une contrainte à un champ Pydantic, et la documentation la montre. Cela se produit parce que Jeroboam lit en direct de votre code.

## Une note sur le rôle de Pydantic

Pydantic gère bien la validation : coercition de type, vérification des contraintes, validation de modèle imbriquée, unions discriminantes, champs calculés, et bien plus encore.

Jeroboam s'appuie dessus, coordonnant entre le cycle requête/réponse de Flask et la validation de Pydantic. Vous n'écrivez pas de code de validation : vos indices de type et modèles Pydantic sont la spécification, et Pydantic les applique automatiquement.

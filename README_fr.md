<div align="center">
    <img
        src="https://github.com/jcbianic/flask-jeroboam/blob/main/docs/_static/img/jeroboam_logo_with_text.png"
        width="400px"
        alt="jeroboam-logo">
    </img>
</div>
<h1 align="center">Flask-Jeroboam</h1>

<p align="center">
    <a href="README.md">English</a> | <a href="README_fr.md">Français</a>
</p>

<div align="center">

<i>Flask-Jeroboam est une extension Flask inspirée de FastAPI. Elle utilise Pydantic pour fournir une validation des données facile à configurer lors de l'analyse des requêtes et de la sérialisation des réponses.</i>

[![PyPI](https://img.shields.io/pypi/v/flask-jeroboam.svg)][pypi_]
[![Python Version](https://img.shields.io/pypi/pyversions/flask-jeroboam)][python version]
[![Download](https://img.shields.io/pypi/dm/flask-jeroboam)][downloads]
[![License](https://img.shields.io/github/license/jcbianic/flask-jeroboam?color=green)][license]
[![Commit](https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam?color=green)][commit]

[![Read the documentation at https://flask-jeroboam.readthedocs.io/](https://img.shields.io/readthedocs/flask-jeroboam/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Maintainability](https://api.codeclimate.com/v1/badges/181b7355cee7b1316893/maintainability)](https://img.shields.io/codeclimate/maintainability/jcbianic/flask-jeroboam?color=green)
[![Test Coverage](https://api.codeclimate.com/v1/badges/181b7355cee7b1316893/test_coverage)](https://img.shields.io/codeclimate/coverage/jcbianic/flask-jeroboam?color=green)
[![Tests](https://github.com/jcbianic/flask-jeroboam/workflows/Tests/badge.svg)][tests]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/flask-jeroboam/
[status]: https://pypi.org/project/flask-jeroboam/
[downloads]: https://img.shields.io/pypi/dm/flask-jeroboam
[python version]: https://pypi.org/project/flask-jeroboam
[read the docs]: https://flask-jeroboam.readthedocs.io/
[tests]: https://github.com/jcbianic/flask-jeroboam/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/jcbianic/flask-jeroboam
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[commit]: https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam

</div>

---

**Documentation**: [https://flask-jeroboam.readthedocs.io/](https://flask-jeroboam.readthedocs.io/)

**Code Source**: [https://github.com/jcbianic/flask-jeroboam](https://github.com/jcbianic/flask-jeroboam)

---

Flask-Jeroboam est une couche légère au-dessus de Flask pour rendre l'analyse des requêtes, la sérialisation des réponses et l'auto-documentation aussi fluides et faciles que dans FastAPI.

## Fonctionnalités Principales

- **Analyse Automatique des Requêtes**: Analyse et validation des données de requête en utilisant les annotations de type des arguments d'endpoint
- **Sérialisation des Réponses**: Sérialisez sans effort les réponses avec les modèles Pydantic
- **Auto-Documentation OpenAPI**: Générez automatiquement une documentation API interactive
- **Sécurité des Types**: Exploitez les annotations de type Python pour un code robuste et auto-documenté
- **Compatible Flask**: Remplacement direct pour les applications Flask avec une compatibilité ascendante complète

## Installation

Vous pouvez installer _flask-jeroboam_ via [pip] ou tout autre outil connecté à [PyPI]:

```console
$ pip install flask-jeroboam
```

## Démarrage Rapide

### Un exemple simple

_Flask-Jeroboam_ sous-classe à la fois les classes Flask et Blueprint. Cela signifie que **Jeroboam** et **Blueprint** se comporteront exactement comme leurs homologues Flask à moins que vous n'activiez leurs comportements spécifiques.

```python
from flask_jeroboam import Jeroboam

app = Jeroboam()

@app.get("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run()
```

Cet exemple simple fonctionnerait exactement comme une application Flask classique. Si vous exécutez ce fichier, alors appeler l'endpoint avec `curl localhost:5000/ping` retournerait la réponse texte `pong`.

Essayons un exemple plus significatif et pertinent en construisant un endpoint simplifié pour récupérer une liste de vins. Nous sommes sur le thème du vin, après tout.

### Recherche de vins

Considérons un endpoint qui fournit une capacité de recherche sur un référentiel de vins. Il analyse et valide trois arguments de la chaîne de requête et les transmet à une fonction CRUD `get_wines` qui retourne une liste de vins sous forme de dictionnaires.
De plus, cet endpoint n'a besoin de retourner que le nom de la cuvée et l'appellation, et d'écarter toute autre information. Voyons à quoi cela pourrait ressembler:

```python
from flask_jeroboam import Jeroboam, InboundModel, OutboundModel
from pydantic.fields import Field
from typing import List, Optional
from docs_src.readme.crud import get_wines

app = Jeroboam(__name__)


class GenericPagination(InboundModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class WineOut(OutboundModel):
    cuvee: str
    appellation: str


@app.get("/wines", response_model=List[WineOut])
def read_wine_list(pagination: GenericPagination, search: Optional[str]):
    wines = get_wines(pagination, search)
    return wines


if __name__ == "__main__":
    app.run()
```

Une fois que vous avez démarré votre serveur, alors appeler l'endpoint avec `curl "localhost:5000/wines?page=1&perPage=2&search=Champagne"` retournerait:

```json
[
  {
    "cuvee": "Brut - Blanc de Blancs",
    "appellation": "Champagne"
  },
  {
    "cuvee": "Grande Cuvée - 170ème Edition",
    "appellation": "Champagne"
  }
]
```

Tous les exemples de la documentation se trouvent dans le dossier `docs_src/X` et devraient fonctionner tels quels. Leurs tests correspondants se trouvent dans `tests/test_docs/X`.

Consultez la documentation pour une utilisation plus avancée: [https://flask-jeroboam.readthedocs.io/](https://flask-jeroboam.readthedocs.io/)

## Pourquoi Flask-Jeroboam?

Je voulais simplement utiliser **la méthode de FastAPI** pour définir les arguments de vue et les modèles de réponse sans quitter Flask.

## Un mot sur les performances

Une chose que **Flask-Jeroboam** ne vous apportera pas, c'est une amélioration des performances. En dessous, Flask et werkzeug gèrent toujours le gros du travail d'un wsgi, donc la transition vers **Flask-Jeroboam** n'accélérera pas votre application. N'oubliez pas que les performances de FastAPI proviennent de Starlette, pas de FastAPI lui-même.

## Public cible

Le public cible de **Flask-Jeroboam** est constitué de développeurs Flask qui trouvent FastAPI très convaincant mais qui ont également d'excellentes raisons de rester avec Flask.

## À propos du nom du projet

Un **Jeroboam** est une grande bouteille, ou flacon, contenant 5 litres de vin[^1], au lieu de 0,75. Les vignerons utilisent ce format pour les vins fins destinés au vieillissement car il offre de meilleures conditions de vieillissement. Premièrement, le rapport entre le volume de vin qu'il contient et la surface d'échange entre le vin et l'air est plus favorable et ralentit la réaction d'oxydation. Ces contenants plus grands mettent également plus de temps à refroidir ou à se réchauffer, ce qui entraîne moins de violence thermique pour le vin pendant la conservation.

En d'autres termes, ce sont des flacons plus durables pour les vins fins. L'intention est de tenir cette promesse pour les APIs.

Le nom sur le thème du vin est un hommage à la startup de technologie vinicole basée à Bordeaux où le développement de ce package a commencé.

[^1]: En dehors de la région de Bordeaux, les bouteilles Jeroboam contiennent 3 litres, comme en Bourgogne ou en Champagne.

## Licence

Distribué sous les termes de la [licence MIT][license], **Flask-Jeroboam** est un logiciel gratuit et open-source.

## Problèmes

Si vous rencontrez des problèmes, veuillez [ouvrir un ticket][file an issue] en suivant les modèles disponibles. Des modèles sont disponibles pour les demandes de fonctionnalités, les rapports de bugs, les mises à jour de documentation et les améliorations d'implémentation.

## Crédits

L'inspiration principale pour ce projet provient de [FastAPI] de [@tiangolo].
À partir de la v0.1.0, il inclut également du code forké de [FastAPI].
Les crédits appropriés sont ajoutés aux docstrings des modules ou des fonctions.

[Flask] et [pydantic] sont les deux dépendances directes et font la plupart du travail.

J'ai utilisé le modèle [Hypermodern Python Cookiecutter] de [@cjolowicz] pour générer ce projet.

[@cjolowicz]: https://github.com/cjolowicz
[@tiangolo]: https://github.com/tiangolo
[fastapi]: https://fastapi.tiangolo.com/
[starlette]: https://www.starlette.io/
[flask]: https://flask.palletsprojects.com/
[pydantic]: https://pydantic-docs.helpmanual.io/
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/jcbianic/flask-jeroboam/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/jcbianic/flask-jeroboam/blob/main/LICENSE
[contributor guide]: https://github.com/jcbianic/flask-jeroboam/blob/main/CONTRIBUTING.md
[command-line reference]: https://flask-jeroboam.readthedocs.io/en/latest/usage.html

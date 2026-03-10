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

<i>Utilisez la syntaxe élégante de FastAPI dans vos applications Flask.</i>

[![PyPI](https://img.shields.io/pypi/v/flask-jeroboam.svg)][pypi_]
[![Python Version](https://img.shields.io/pypi/pyversions/flask-jeroboam)][python version]
[![Download](https://img.shields.io/pypi/dm/flask-jeroboam)][downloads]
[![License](https://img.shields.io/github/license/jcbianic/flask-jeroboam?color=green)][license]
[![Commit](https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam?color=green)][commit]

[![Read the documentation at https://flask-jeroboam.readthedocs.io/](https://img.shields.io/readthedocs/flask-jeroboam/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Coverage](https://codecov.io/gh/jcbianic/flask-jeroboam/graph/badge.svg)][codecov]
[![Tests](https://github.com/jcbianic/flask-jeroboam/workflows/Tests/badge.svg)][tests]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)][ruff]

[pypi_]: https://pypi.org/project/flask-jeroboam/
[status]: https://pypi.org/project/flask-jeroboam/
[downloads]: https://img.shields.io/pypi/dm/flask-jeroboam
[python version]: https://pypi.org/project/flask-jeroboam
[read the docs]: https://flask-jeroboam.readthedocs.io/
[tests]: https://github.com/jcbianic/flask-jeroboam/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/jcbianic/flask-jeroboam
[pre-commit]: https://github.com/pre-commit/pre-commit
[ruff]: https://github.com/astral-sh/ruff
[commit]: https://img.shields.io/github/last-commit/jcbianic/flask-jeroboam

</div>

---

**Documentation** : [https://flask-jeroboam.readthedocs.io/](https://flask-jeroboam.readthedocs.io/)

**Code source** : [https://github.com/jcbianic/flask-jeroboam](https://github.com/jcbianic/flask-jeroboam)

---

## Qu'est-ce que Flask-Jeroboam ?

Flask-Jeroboam amène l'approche de FastAPI à Flask. Vous aimez comment FastAPI gère la validation des requêtes, la validation des réponses et la documentation automatique, mais vous avez besoin (ou préférez) Flask ? C'est pour vous.

Il examine les signatures de vos fonctions d'endpoint et gère automatiquement la validation, la sérialisation et la génération de documentation OpenAPI. C'est simplement une couche fine qui connecte Flask à Pydantic comme FastAPI le fait.

## Pourquoi Flask-Jeroboam ?

**Vous avez du code Flask existant** — Refactoriser vers FastAPI n'est pas envisageable. Jeroboam s'intègre directement.

**Vous dépendez de l'écosystème Flask** — Flask-SQLAlchemy, Flask-Login, Flask-Admin et des dizaines d'autres extensions marchent simplement. FastAPI ne fonctionne pas avec eux.

**Vous servez à la fois du HTML et des APIs** — Certaines applications ont besoin de rendre des templates aux côtés des endpoints JSON. Flask gère les deux sans problème.

**Vous préférez WSGI** — Que ce soit pour l'infrastructure ou la préférence d'équipe, WSGI est votre modèle de déploiement.

**Vous voulez l'expérience de FastAPI** — Des endpoints type-safe avec documentation automatique, sans changer de framework.

## Fonctionnalités clés

- **Validation par paramètre** — Les indices de type sur les arguments d'endpoint valident et analysent automatiquement les données de requête
- **Validation des réponses** — Définissez des modèles de réponse ; Jeroboam valide que les données sortantes correspondent au schéma
- **Documentation OpenAPI automatique** — Documentation d'API interactive générée automatiquement
- **Sécurité des types** — Utilisez les indices de type Python pour clarifier le code et détecter les bugs plus tôt
- **Compatible clé en main** — Fonctionne avec les applications Flask existantes et les extensions

## Installation rapide

```console
$ pip install flask-jeroboam
```

Guide d'installation complet avec gestion des dépendances : [Installation](https://flask-jeroboam.readthedocs.io/en/latest/installation.html)

## Prochaines étapes

**Nouveau chez Jeroboam ?** Commencez par le guide [Bien démarrer](https://flask-jeroboam.readthedocs.io/en/latest/getting_started.html).

**Prêt à construire ?** Suivez le [Tutoriel](https://flask-jeroboam.readthedocs.io/en/latest/tutorial/index.html) pour un exemple complet.

**Besoin de détails spécifiques ?** Consultez les [Guides pratiques](https://flask-jeroboam.readthedocs.io/en/latest/guides/index.html) pour les tâches courantes.

**Voulez vous approfondir votre compréhension ?** Lisez la section [Concepts](https://flask-jeroboam.readthedocs.io/en/latest/concepts/index.html).

## Comment ça se compare ?

Flask-Jeroboam occupe une place particulière dans le paysage, plus proche de FastAPI que de flask-openapi3 ou flask-restx, mais solidement dans l'écosystème Flask.

| Aspect | Jeroboam | flask-openapi3 | FastAPI |
|--------|----------|---|---------|
| Indices par paramètre | ✅ | ❌ (groupés dans les modèles) | ✅ |
| Validation des réponses | ✅ par défaut | ⚠️ optionnel | ✅ par défaut |
| Pydantic v2 | ✅ | ✅ | ✅ |
| Composition de décorateurs | ✅ | ❌ | ✅ |
| Compatible Flask | ✅ | ✅ | ❌ (framework séparé) |
| Async/await | ❌ (WSGI) | ❌ (WSGI) | ✅ (ASGI) |

Voir le guide complet de [Comparaison](https://flask-jeroboam.readthedocs.io/en/latest/alternatives.html) pour une analyse détaillée.

## À propos du nom

Un Jeroboam est une grande bouteille de vin (5 litres en Bordelais, 3 litres ailleurs) conçue pour les vins fins qui vieillissent bien. Le rapport surface-volume plus grand ralentit l'oxydation. La température reste plus stable. Elles durent sans abîmer le vin.

Le projet vise la même durabilité : une API qui reste solide et fiable en vieillissant.

## Licence

Distribué sous les termes de la [Licence MIT][license]. Flask-Jeroboam est un logiciel libre et open source.

## Problèmes

Vous avez trouvé un bug ou voulez suggérer une fonctionnalité ? Veuillez [signaler un problème](https://github.com/jcbianic/flask-jeroboam/issues) en utilisant les modèles disponibles.

## Crédits

Inspiré par [FastAPI](https://fastapi.tiangolo.com/) de [@tiangolo](https://github.com/tiangolo).

Construit avec [Flask](https://flask.palletsprojects.com/) et [Pydantic](https://docs.pydantic.dev/) — deux excellents projets.

[license]: https://github.com/jcbianic/flask-jeroboam/blob/main/LICENSE

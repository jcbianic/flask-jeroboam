# Guide du contributeur

J'apprécie votre intérêt à améliorer ce projet. Ce projet est open-source sous la [licence MIT] et
accueille les contributions sous forme de rapports de bogues, de demandes de fonctionnalités et de demandes d'extraction. Actuellement, notre focus est sur **l'amélioration de la documentation** et **la chasse aux bogues**.

Nous avons l'intention d'utiliser le [Suivi des problèmes] pour coordonner la communauté et fournir des modèles pour les rapports de bogues, les demandes de fonctionnalités, les mises à jour de documentation et les améliorations d'implémentation. Assurez-vous donc d'utiliser le modèle approprié avec les instructions supplémentaires.

## Ressources

Voici une liste de ressources importantes pour les contributeurs :

- [Code Source]
- [Documentation]
- [Suivi des problèmes]
- [Code de Conduite]

[licence mit]: https://opensource.org/licenses/MIT
[code source]: https://github.com/jcbianic/flask-jeroboam
[documentation]: https://flask-jeroboam.readthedocs.io/
[suivi des problèmes]: https://github.com/jcbianic/flask-jeroboam/issues

## Comment configurer votre environnement de développement

Vous avez besoin de Python 3.10+ et d'[uv] :

```console
$ uv sync --group dev
```

Vous pouvez maintenant exécuter une session Python interactive,
ou l'interface de la ligne de commande :

```console
$ uv run python
$ uv run flask-jeroboam
```

[uv]: https://docs.astral.sh/uv/
[nox]: https://nox.thea.codes/

## Comment tester le projet

uv gère les versions de Python et les environnements virtuels automatiquement. Pour exécuter toutes les sessions nox sur toutes les versions Python supportées (3.10–3.13), assurez-vous que les versions cibles sont disponibles :

```bash
uv python install 3.10 3.11 3.12 3.13
```

Puis exécutez toutes les sessions nox :

```bash
nox
```

Si vous voulez exécuter une session nox spécifique, faites :

```bash
nox --session "pre-commit"
```

Exécutez la suite de tests complète :

```console
$ nox
```

Listez les sessions Nox disponibles :

```console
$ nox --list-sessions
```

Vous pouvez aussi exécuter une session Nox spécifique.
Par exemple, invoquez la suite de tests unitaires comme ceci :

```console
$ nox --session=tests
```

Les tests unitaires sont situés dans le répertoire _tests_,
et sont écrits en utilisant le framework de test [pytest].

[pytest]: https://pytest.readthedocs.io/

## Comment soumettre des modifications

Ouvrez une [demande d'extraction] pour soumettre des modifications à ce projet.

Votre demande d'extraction doit respecter les directives suivantes pour être acceptée :

- La suite de tests Nox doit passer sans erreurs ni avertissements.
- Inclure des tests unitaires. Ce projet maintient 100% de couverture de code.
- Si vos modifications ajoutent des fonctionnalités, mettez à jour la documentation en conséquence.

N'hésitez pas à soumettre tôt, cependant — nous pouvons toujours itérer sur cela.

Pour exécuter les vérifications de lint et de formatage du code avant de valider votre modification, vous pouvez installer pre-commit comme un hook Git en exécutant la commande suivante :

```console
$ nox --session=pre-commit -- install
```

Il est recommandé d'ouvrir un problème avant de commencer à travailler sur quoi que ce soit.
Cela permettra une chance de discuter avec les propriétaires et valider votre approche.

[demande d'extraction]: https://github.com/jcbianic/flask-jeroboam/pulls

<!-- github-only -->

[code de conduite]: ../../CODE_OF_CONDUCT.md

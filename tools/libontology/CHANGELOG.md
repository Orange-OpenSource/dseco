# Changelog

Toutes les modifications notables apportées à ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet adhère à [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-28
- add libontology-bulk_update

## [1.0.0] - 2026-10-08
- add libontology-compare

## [0.9.3] - 2026-10-08
- weird bug when the ontology file was not found, it was still working :-)

## [0.9.2] - 2026-10-07
- bug

## [0.9.1] - 2026-10-07
- Add defusedxml

## [0.9.0] - 2026-10-07
- Add owlrl inference by default to `libontology-*` (OWL-RL inference before the query/update)

## [0.8.0] - 2026-10-06
- Add owlrl inference with --infer, it was a bad idea

## [0.7.2] - 2026-10-06
- owlready to 0.51

## [0.7.1] - 2026-10-06
- Add `--version` option to all scripts (`libontology-query`, `-describe`, `-ask`, `-infer`, `-validate`, `-shacl`, `-update`, `-convert-ttl-to-xmlrdf`, `-convert-xmlrdf-to-ttl`, `-pull`, `-add_swrl_rule`, `-stats`, `-smart-diff`)
- `libontology-pull` now parses its command line (`--help`, `--version`)
- Expose `libontology.__version__`

## [0.7.0] - 2026-06-09
- Deleted catalog loading because there is a path issue for the moment

## [0.6.9] - 2026-06-05
- Added catalog loading
- Add libontology-smart-diff

## [0.6.8] - 2025-09-02
- Add libontology-stats

## [0.6.7] - 2025-06-05
- didier rename `libontology_tests` par `tests`

## [0.6.6] - 2025-05-26
- didier create an opensource version

## [0.6.0] - 2025-02-13
- didier Add libontology-describe 

## [0.5.0] - 2025-02-13
- antoine Add libontology-shacl 

## [0.3.3] - 2024-05-16
- Add Unit tests

## [0.1.1] - 2024-04-15
- Ajout de la commande `libontology-update` pour exécuter des requêtes SPARQL UPDATE.
- Ajout de la commande `libontology-infer` pour exécuter une inférence OWL RL.
- Ajout de la commande `libontology-convert-ttl-to-xmlrdf` pour convertir une ontologie du format Turtle au format RDF/XML.
- Ajout de la commande `libontology-pull` pour télécharger et mettre à jour une ontologie depuis une URL.
- Ajout de la commande `libontology-validate` pour valider une ontologie.

## [0.1.0] - 2024-04-15
- Création initiale du package `libontology`.
- Implémentation de la classe abstraite `BaseOntology`.
- Implémentation des classes `OntologyQuery` et `OntologyAsk` héritant de `BaseOntology`.
- Configuration du fichier `setup.py` pour l'installation du package.
- Ajout d'un fichier `README.md` pour la documentation du projet.
- Ajout de la commande `libontology-query` pour exécuter des requêtes SPARQL SELECT.
- Ajout de la commande `libontology-ask` pour exécuter des requêtes SPARQL ASK.

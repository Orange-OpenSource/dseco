# DNS Security Ontology (DSecO) -- libontology

`libontology` est un package Python conçu pour faciliter l'interrogation, la mise à jour, la validation et la conversion des ontologies en utilisant le langage SPARQL et d'autres opérations liées aux ontologies.

## Fonctionnalités

- Interrogation d'ontologies avec SPARQL SELECT (`libontology-query`)
- Exécution de requêtes SPARQL ASK (`libontology-ask`)
- Inférence (Hermit/Pellet/OWL RL) (`libontology-infer`)
- Validation d'ontologies (`libontology-validate`)
- Mise à jour d'ontologies avec SPARQL UPDATE (`libontology-update`)
- Conversion de formats d'ontologies (`libontology-convert-ttl-to-xmlrdf`)
- Conversion de formats d'ontologies (`libontology-convert-xmlrdf-to-ttl`)
- Téléchargement et mise à jour de l'ontologie depuis une URL (`libontology-pull`)
- Validation de la terminologie (`libontology-shacl`)
- Description d'éléments de l'ontologie (`libontology-describe`)
- Ajout de règle SWRL utile pour l'inférence (`libontology-convert-add_swrl_rule`)

## Utilisation

Après l'installation, vous pouvez utiliser les différentes commandes directement depuis votre terminal.

### Interroger une ontologie

Pour exécuter une requête SPARQL SELECT sur une ontologie :

```bash
libontology-query --ontology chemin_vers_ontologie --query chemin_vers_requete_sparql
```

### Exécuter une requête ASK

Pour exécuter une requête SPARQL ASK sur une ontologie :

```bash
libontology-ask --ontology chemin_vers_ontologie --query chemin_vers_requete_ask
```

### Effectuer une inférence 

Pour effectuer une inférence sur une ontologie (Hermit/Pellet/OWL RL):

```bash
libontology-infer --ontology chemin_vers_ontologie --destination chemin_vers_ontologie_inferee --reasoner nom_du_raisonneur
```

### Valider une ontologie

Pour valider une ontologie :

```bash
libontology-validate --ontology chemin_vers_ontologie
```

### Mettre à jour une ontologie avec SPARQL UPDATE

Pour mettre à jour une ontologie en utilisant une requête SPARQL UPDATE :

```bash
libontology-update --ontology chemin_vers_ontologie --query chemin_vers_requete_update --destination chemin_vers_ontologie_mise_a_jour
```

### Convertir des formats d'ontologies

Pour convertir une ontologie du format Turtle au format RDF/XML :

```bash
libontology-convert-ttl-to-xmlrdf --ontology chemin_vers_ontologie_turtle --destination chemin_vers_ontologie_xmlrdf
```

### Valider la partie terminologique d'une ontologie

Pour valider la partie terminologique (les contraintes, les restrictions, ...) d'une ontologie :

```bash
libontology-shacl --ontology chemin_vers_ontologie --shacl chemin_vers_graphe_shacl
```

### Exécuter une requête DESCRIBE

Pour exécuter une requête SPARQL DESCRIBE sur une ontologie :

```bash
libontology-describe --ontology chemin_vers_ontologie --query chemin_vers_requete_describe
```

### Ajouter une SWRL rule

Pour ajouter une SWRL rule sur une ontologie :

```bash
libontology-add_swrl_rule --ontology chemin_vers_ontologie --rulefile chemin_vers_regle_SWRL --destination chemin_vers_ontologie_avec_regle
```


# libontology

`libontology` is a Python package designed to ease querying, updating, validating and converting ontologies using the SPARQL language and other ontology-related operations.

## Features

- Query ontologies with SPARQL SELECT (`libontology-query`)
- Run SPARQL ASK queries (`libontology-ask`)
- Inference (Hermit/Pellet/OWL RL) (`libontology-infer`)
- Ontology validation (`libontology-validate`)
- Update ontologies with SPARQL UPDATE (`libontology-update`)
- Ontology format conversion (`libontology-convert-ttl-to-xmlrdf`)
- Ontology format conversion (`libontology-convert-xmlrdf-to-ttl`)
- Download and update the ontology from a URL (`libontology-pull`)
- Terminology validation (`libontology-shacl`)
- Description of ontology elements (`libontology-describe`)
- Add a SWRL rule, useful for inference (`libontology-convert-add_swrl_rule`)

## Usage

After installation, you can use the various commands directly from your terminal.

### Query an ontology

To run a SPARQL SELECT query on an ontology:

```bash
libontology-query --ontology path_to_ontology --query path_to_sparql_query
```

### Run an ASK query

To run a SPARQL ASK query on an ontology:

```bash
libontology-ask --ontology path_to_ontology --query path_to_ask_query
```

### Perform inference

To perform inference on an ontology (Hermit/Pellet/OWL RL):

```bash
libontology-infer --ontology path_to_ontology --destination path_to_inferred_ontology --reasoner reasoner_name
```

### Validate an ontology

To validate an ontology:

```bash
libontology-validate --ontology path_to_ontology
```

### Update an ontology with SPARQL UPDATE

To update an ontology using a SPARQL UPDATE query:

```bash
libontology-update --ontology path_to_ontology --query path_to_update_query --destination path_to_updated_ontology
```

### Convert ontology formats

To convert an ontology from Turtle to RDF/XML:

```bash
libontology-convert-ttl-to-xmlrdf --ontology path_to_turtle_ontology --destination path_to_xmlrdf_ontology
```

### Validate the terminological part of an ontology

To validate the terminological part (constraints, restrictions, ...) of an ontology:

```bash
libontology-shacl --ontology path_to_ontology --shacl path_to_shacl_graph
```

### Run a DESCRIBE query

To run a SPARQL DESCRIBE query on an ontology:

```bash
libontology-describe --ontology path_to_ontology --query path_to_describe_query
```

### Add a SWRL rule

To add a SWRL rule to an ontology:

```bash
libontology-add_swrl_rule --ontology path_to_ontology --rulefile path_to_swrl_rule --destination path_to_ontology_with_rule
```


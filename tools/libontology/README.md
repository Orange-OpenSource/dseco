# DNS Security Ontology (DSecO) -- libontology

`libontology` is a Python package designed to facilitate querying, updating, validating, and converting ontologies using SPARQL language and other ontology-related operations.

## Features

- Query ontologies with SPARQL SELECT (`libontology-query`)
- Execute SPARQL ASK queries (`libontology-ask`)
- Perform inference (Hermit/Pellet/OWL RL) (`libontology-infer`)
- Validate ontologies (`libontology-validate`)
- Update ontologies with SPARQL UPDATE (`libontology-update`)
- Convert ontology formats (`libontology-convert-ttl-to-xmlrdf`, `libontology-convert-xmlrdf-to-ttl`)
- Download and update ontology from a URL (`libontology-pull`)
- Validate terminology (`libontology-shacl`)
- Describe ontology elements (`libontology-describe`)
- Add useful SWRL rules for inference (`libontology-convert-add_swrl_rule`)

## Usage

After installation, commands can be run directly from the terminal.

### Query an ontology

To execute a SPARQL SELECT query:

```bash
libontology-query --ontology path_to_ontology --query path_to_sparql_query
```

### Execute an ASK query

```bash
libontology-ask --ontology path_to_ontology --query path_to_ask_query
```

### Perform inference

```bash
libontology-infer --ontology path_to_ontology --destination path_to_inferred_ontology --reasoner reasoner_name
```

### Validate an ontology

```bash
libontology-validate --ontology path_to_ontology
```

### Update an ontology with SPARQL UPDATE

```bash
libontology-update --ontology path_to_ontology --query path_to_update_query --destination path_to_updated_ontology
```

### Convert ontology formats

From Turtle to RDF/XML:

```bash
libontology-convert-ttl-to-xmlrdf --ontology path_to_turtle_ontology --destination path_to_xmlrdf
```

### Validate terminology part of an ontology

```bash
libontology-shacl --ontology path_to_ontology --shacl path_to_shacl_graph
```

### Execute a DESCRIBE query

```bash
libontology-describe --ontology path_to_ontology --query path_to_describe_query
```

### Add a SWRL rule

```bash
libontology-add_swrl_rule --ontology path_to_ontology --rulefile path_to_swrl_rule --destination path_to_ontology_with_rule
```

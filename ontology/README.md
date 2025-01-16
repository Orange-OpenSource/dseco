# DSecO / ontology files repository

This folder contains the **DSecO ontology documents**.

We provide a direct access to the DSecO resources with the **dseco** [w3id.org](https://w3id.org/) identifier:
> [https://w3id.org/dseco/](https://w3id.org/dseco/)

Based on this identifier, the **[https://w3id.org/dseco/ontology/](https://w3id.org/dseco/ontology/)** URI refers to the ontology itself.

Details below provide directions for the ontology implementation.

## Naming convention

Each ontology document must be in [Turtle](https://www.w3.org/TR/turtle/) syntax, and saved in a folder whose name corresponds to the version of the data model:

```
NAME-MAJOR.MINOR/DOCUMENT.ttl
```

where:

- NAME matches `^[a-z]*$`
- MAJOR matches `^[0-9]+$`
- MINOR matches `^[0-9]+$`

see http://semver.org/ for semantic versioning specification.

When releasing a new version of the ontology,

* create a `dseco-<major>.<minor>` folder,
* update the `dseco-latest.ttl` symbolic link for targeting the latest ontology version:
	```shell
	# From the ontology directory
	ln -s -f dseco-<MAJOR.MINOR>/dseco.ttl dseco-latest.ttl
	# e.g. ln -s -f dseco-1.5/dseco.ttl dseco-latest.ttl
	```

Direct reference to a versioned ontology implementation also makes use of the *dseco* identifier.
For example, the v1.5 main ontology file is available at: [https://w3id.org/dseco/ontology/dseco-1.5](https://w3id.org/dseco/ontology/dseco-1.5).
Using this approach rely on rewriting rules defined at the [perma-id/w3id.org](https://github.com/perma-id/w3id.org) level towards the relevant folder/sub-folder.

## Ontology metadata

An ontology instance uses the following metadata:

- type `owl:Ontology`;
- a `owl:versionIRI` equal to `<https://w3id.org/dseco/ontology/NAME-MAJOR.MINOR>`;
- a `owl:versionInfo` that starts with `"vMAJOR.MINOR"`;
- potentially, a `owl:priorVersion`;
- zero or more `owl:import`s that point to other ontologies (potentially ontology version IRIs) to be imported.

Then each ontology instance must have the following recommended metadata:

- type `voaf:Vocabulary`;
- at least one `dcterms:title` with a language tag;
- at least one `dcterms:description` with a language tag (it SHOULD use the markdown syntax);
- a `dcterms:issued` (some `xsd:date`);
- a `dcterms:modified` (some `xsd:date`);
- a `dcterms:creator` (some `foaf:Person`);
- zero or more `dcterms:contributor` (some `foaf:Person`);
- a `cc:licence` equal to `<https://spdx.org/licenses/BSD-4-Clause>`;
- a `vann:preferredNamespacePrefix` equal to `"dseco"`;
- a `vann:preferredNamespaceUri` equal to `<https://w3id.org/dseco/ontology/>`;

## Concept metadata

Every other resource in the ontology `<https://w3id.org/dseco/ontology/SOME_RESOURCE>` must have the following metadata:

- at least one `rdfs:label`;
- at least one `rdfs:comment` with a language tag (it SHOULD use the [Markdown](https://www.markdownguide.org/) syntax);
- a `vs:term_status`: one of `"unstable"`, `"testing"`, or `"stable"`;
- a `rdfs:isDefinedBy` equal to `dseco:`.

## Alignment to other data models

Alignment to other data models should be defined within each ontology file at the concept or property level.

If weak coupling between the ontology and alignment implementations is required, then alignment to other data models should be defined in independent files, and be named as follows:

```
<SCHEMA>Alignement-MAJOR.MINOR.ttl
```

If precise vocabulary/concept alignment is not defined, concepts should at least have an "*alignment reference*" in its `rdfs:comment` metadata (e.g. "*this concept is partially in line with the semantics of `bot:Site`*").

## References

See the following links for useful details:

* Daniel Garijo and María Poveda-Villalón. A checklist for complete vocabulary metadata. URL: https://w3id.org/widoco/bestPractices

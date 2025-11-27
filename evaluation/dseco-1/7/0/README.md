# DNS Security Ontology (DSecO) -- unit tests

This folder holds authoring tests for evaluating the DSecO implementation through a unit test approach.
Authoring tests also reflects DNS audit application queries, thus can also serve as example queries to run on a DNS-KG structured by DSecO.

## Usage

### Implementing unittests

- Create a folder for the specific test case in the [queries/](queries/) folder, e.g. `./queries/test_01`
- Create a file for the test with the `test.sparql` name
- Define the test case in `test.sparql`
- Implement the test as a [SPARQL](https://www.w3.org/TR/sparql11-overview/) query in `test.sparql`
- Implement the test result baseline in `test.csv`
- Define the scenario satisfied by the test case in [features/test_ontology.feature](features/test_ontology.feature), following the [Gherkin](https://cucumber.io/docs/gherkin/) syntax or the Behave syntax.

### Running unittests

Pre-requisites:

- Install the *libontology* package to enable calling the *libontology-infer* and *libontology-query* commands.
- Build the datatest by using the following commands (make sure to place yourself inside the unittests folder):
```shell
./builder.sh builder/retrievers/ datatest_rml.ttl builder/cleaners
```
    

Running tests:

```shell
# From the local directory
./unittests_all.sh
```

Test sources one by one
```
unittests.by_source.sh
```

Testing builder against `datatest_rml.ttl`
```
unittests_builder.sh
```

Then testing queries
```
unittests.queries.sh
unittests.behave.sh
```



The script runs all SPARQL queries to be found in the current sub-folders against the [dataset.ttl](datatest.ttl) knowledge graph example.
For each test case, the query results are compared to the stored result baseline; an alert is raised if any difference is found.

### Running the feature check

TBC.

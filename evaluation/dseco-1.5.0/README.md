# DNS Security Ontology (DSecO) -- v1.5.0 unit tests & assessment cases

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

### Next steps

- Running the feature check <= leverages the tests from the `features` folder, and *test* queries from the `queries` folder.
- Running unittests <= leverages the *uc* queries from the `queries` folder.

... both steps leverage the [dataset.ttl](datatest.ttl) file from the current folder.

### Running unittests
`./unittests.sh` : will run a test for each directory in `queries` directory

### Notes

- Folder and file names in the subfolders are as follows: `test_xxx` or `uc_xxx`
  - `uc_xxx` are described in the DSecO paper,
  - `test_xxx` are just for implementation testing purpose.

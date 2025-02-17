# language: en

Feature: Functional test on a test ontology.

  Scenario: I have many FQDN with a WhoisDomain which is example.org
    Given that the KG is loaded and the reasoner applied
    When I run SPARQL query located at queries/test_example.org_entries/test.sparql to gather entries with WhoisDomain is example.org
    Then I should obtain the results from file queries/test_example.org_entries/test.csv

  Scenario: Récupérer les entrées de la zone example.org avec leur résolution finale
    Given that the KG is loaded and the reasoner applied
    When I run SPARQL query located at queries/test_entries_with_resolution/test.sparql to gather entries with WhoisDomain is example.org and their final resolution
    Then I should obtain the results from file queries/test_entries_with_resolution/test.csv

  Scenario: Search for FQDN that belongs to zone example.org and that have a FQDN intermediary or final witch is not managed by Org top nor Org int
    Given that the KG is loaded and the reasoner applied
    When I run SPARQL query located at queries/uc_domain_hijacking/test.sparql to gather FQDN belongings to zone example.org and that a intermediary or final witch is not managed by Org top nor Org int
    Then I should obtain the results from file queries/uc_domain_hijacking/test.csv

  Scenario: Search for FQDN that belongs to zone example.org and that do not resolve at all at the end
    Given that the KG is loaded and the reasoner applied
    When I run SPARQL query located at queries/uc_ultimately_do_not_resolve_to_an_IP_address/test.sparql to gather entries of example.org that do not resolve at all at the end
    Then I should obtain the results from file queries/uc_ultimately_do_not_resolve_to_an_IP_address/test.csv

  Scenario: Search for FQDN managedBy Org int that do not have a corresponding in Org top
    Given that the KG is loaded and the reasoner applied
    When I run SPARQL query located at queries/uc_complete_cleanup/test.sparql to gather entries managedBy Org int that do not have a corresponding in Org top
    Then I should obtain the results from file queries/uc_complete_cleanup/test.csv

  Scenario: Search for FQDN managedBy Org int that do not have a corresponding in Org top and that have a A to an IP
    Given that the KG is loaded and the reasoner applied
    When I run SPARQL query located at queries/uc_complete_cleanup_not_resolving/test.sparql to gather entries managedBy Org int that do not have a corresponding in Org top and that have a A to an IP
    Then I should obtain the results from file queries/uc_complete_cleanup_not_resolving/test.csv

  Scenario: List all the IP address
    Given that the KG is loaded and the reasoner applied
    When I run SPARQL query located at queries/test_list_all_IP_Address/test.sparql to list all the IP address
    Then I should obtain the results from file queries/test_list_all_IP_Address/test.csv

  Scenario: Search for FQDN that loops to themselves
    Given that the KG is loaded and the reasoner applied
    When I run SPARQL query located at queries/uc_loop/test.sparql to gather entries that loops to themselves
    Then I should obtain the results from file queries/uc_loop/test.csv

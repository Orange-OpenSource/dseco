# CHANGELOG
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Breaking Changes

> **⚠ Warning:** This release contains breaking changes.  
> We assumed these breaking changes because we wanted to rebase our terminology on [W3C standards](https://www.w3.org/).


[v2.0.0] - 2026-06-03
---------------------
- Adapted all queries with the new terminology so we still have security answers
- Pass a check on each query to validate list of PREFIX and Syntax
- Used only camelCase for properties : list of properties and their changes: 
    - is_CNAME_of -> isCNAMEOf
    - is_A_to -> isATo
    - is_AAAA_to -> isAAAATo
    - resolves_to -> resolvesTo
    - is_in_zone -> isInZONE
    - is_CNAME_of_CNAME_of -> isCNAMEOfCNAMEOf
    - is_part_of -> isPartOf
    - is_hosted_by -> isHostedBy
    - is_included_in -> isIncludedIn
    - isinOurSubnet -> isInOurSubnet
    - FQDN_ends_in_exampleorg -> FQDNEndsInExampleorg
    - answers_on_port_443 -> answersOnPort443
    - answers_on_port_80 -> answersOnPort80
    - answers_on_port -> answersOnPort)
- Deleted TAG and hasTag and replaced it by knownFrom and ORGU_team_GCP
- remove requirements.txt for unittests, uv rulez



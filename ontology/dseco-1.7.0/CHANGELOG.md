# CHANGELOG
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

[v1.7.0] - 2025-11-26
---------------------
- Added a datatest's builder based on rml
- Added individuals inside the datatest
- Added rename dseco:whoisdomain in dseco:ZONE
- Added observable:IPAddress observable:IPAddressFacet
- Added observable:IPv4Address observable:IPv6Address
- Added dseco:is_part_of, observable:NetworkSubnet
- Added observable:IPAddress dseco:is_part_of observable:NetworkSubnet
- Added observable:AutonomousSystem core:hasFacet observable:AutonomousSystemFacet
- Added observable:IPAddress dseco:hasAS observable:AutonomousSystem
- Added observable:NetworkSubnet dseco:hasAS observable:AutonomousSystem
- Added observable:AutonomousSystem dseco::originates observable:NetworkSubnet
- Added dseco:CVE
- Added dseco:COMPONENT
- Added dseco:FQDN  dseco:is_hosted_by dseco:COMPONENT
- Added dseco:COMPONENT dseco:is_included_in dseco:COMPONENT
- Added dseco:COMPONENT dseco:dependsOn dseco:COMPONENT
- Added dseco:COMPONENT :hasServiceId xsd:string
- Added dseco:COMPONENT :hasBomRef xsd:string
- Added skos:example in each Classe or Property
- Added SHACL shapes for new properties
- Added rmls mappings to build the toy dataset

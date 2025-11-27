The objective here is just to read the route in this sbom
and build triplets

````
:FQDN :is_hosted_by :COMPONENT
````

````
cat mapping_rml/mapping_routes.ttl | envsubst > /tmp/mapping_routes.ttl

java -jar ../../rmlmapper.jar -m /tmp/mapping_routes.ttl -o /dev/stdout
````

it creates this :

```
<https://w3id.org/dseco/mykg/COMPONENT_cbfad02f9ed2a8d1e08d8f74f5303e9eb93637d47f82ab6f1c15871cf8dd0481> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
<https://w3id.org/dseco/mykg/COMPONENT_cbfad02f9ed2a8d1e08d8f74f5303e9eb93637d47f82ab6f1c15871cf8dd0481> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://w3id.org/dseco/ontology/COMPONENT> .
<https://w3id.org/dseco/mykg/COMPONENT_cbfad02f9ed2a8d1e08d8f74f5303e9eb93637d47f82ab6f1c15871cf8dd0481> <https://w3id.org/dseco/ontology/hasServiceId> "10001212" .
<https://w3id.org/dseco/mykg/FQDN_fqdn1.from_sbom_data> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
<https://w3id.org/dseco/mykg/FQDN_fqdn1.from_sbom_data> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://w3id.org/dseco/ontology/FQDN> .
<https://w3id.org/dseco/mykg/FQDN_fqdn1.from_sbom_data> <https://w3id.org/dseco/ontology/is_hosted_by> <https://w3id.org/dseco/mykg/COMPONENT_cbfad02f9ed2a8d1e08d8f74f5303e9eb93637d47f82ab6f1c15871cf8dd0481> .
<https://w3id.org/dseco/mykg/FQDN_fqdn2.from_sbom_data> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
<https://w3id.org/dseco/mykg/FQDN_fqdn2.from_sbom_data> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://w3id.org/dseco/ontology/FQDN> .
<https://w3id.org/dseco/mykg/FQDN_fqdn2.from_sbom_data> <https://w3id.org/dseco/ontology/is_hosted_by> <https://w3id.org/dseco/mykg/COMPONENT_cbfad02f9ed2a8d1e08d8f74f5303e9eb93637d47f82ab6f1c15871cf8dd0481> .
```

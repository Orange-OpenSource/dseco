The objective here is just to read records, sort on recordtype
and build specific triplets based on recordtype

````
:FQDN :answersOnPort80 "true"^^xsd:boolean
:FQDN :answersOnPort443 "true"^^xsd:boolean
````

````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_httpx.ttl -o /dev/stdout
````
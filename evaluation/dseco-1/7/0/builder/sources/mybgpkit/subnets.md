The objective here is just to read subnets and asn
and build triplets

````
observable:NetworkSubnet :hasAS observable:AutonomousSystem
````

````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_subnets.ttl -o /dev/stdout
````


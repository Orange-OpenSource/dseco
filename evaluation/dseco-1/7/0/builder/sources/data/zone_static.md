The objective here is just to read zones and orgus (zones here are managed by 2 known entities: "top" and "int")
and build triplets

````
:ZONE :managedBy org:OrganizationalUnit
````

````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_zone_int.ttl -o /dev/stdout
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_zone_top.ttl -o /dev/stdout
````


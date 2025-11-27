The objective here is just to read records, sort on recordtype
and build specific triplets based on recordtype

### mapping_a_record:
````
:FQDN :is_in_zone :ZONE
:FQDN :is_A_to observable:IPAddress
````

### mapping_aaaa_record:
````
:FQDN :is_in_zone :ZONE
:FQDN :is_AAAA_to observable:IPAddress
````

### mapping_ipv4 and mapping_ipv6:
````
observable:IPAddress :hasAS observable:AutonomousSystem
````

### mapping_cname:
````
:FQDN :is_CNAME_of :FQDN
````

### mapping_asn:
````
observable:AutonomousSystem :hasOrgu org:OrganizationalUnit
````

### mapping_orgu_asn and mapping_orgu_dynamic:
````
org:OrganizationalUnit a owl:NamedIndividual
````

## Commandes RML

### A record:
````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_a_record.ttl -o /dev/stdout
````

### AAAA record:
````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_aaaa_record.ttl -o /dev/stdout
````

### IPv4:
````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_ipv4.ttl -o /dev/stdout
````

### IPv6:
````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_ipv6.ttl -o /dev/stdout
````

### CNAME:
````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_cname.ttl -o /dev/stdout
````

### ASN:
````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_asn.ttl -o /dev/stdout
````

### Orgu ASN:
````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_orgu_asn.ttl -o /dev/stdout
````

### Orgu Dynamic:
````
java -jar ../../rmlmapper.jar -m mapping_rml/mapping_orgu_dynamic.ttl -o /dev/stdout
````

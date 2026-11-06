The objective here is just to read the route in this sbom
and build triplets


spec is here https://cyclonedx.org/specification/overview/


````
cat mapping_rml/mapping_component_composed_of.ttl | envsubst > /tmp/mapping_component_composed_of.ttl

java -jar ../../rmlmapper.jar -m /tmp/mapping_component_composed_of.ttl -o /dev/stdout
````

it creates this :

```
```


To access both the current component element and metadata, there are two solutions:

1. Use a parent-child TriplesMap (rr:parentTriplesMap)
A parent TriplesMap on "$[*]" (complete SBOM, access to metadata)
A child TriplesMap on "$[*].components[*]" (current component)
Use rr:joinCondition to link the two (for example via a common identifier)


2. Use relative JSONPath (if supported by your RML engine)
Some RML engines allow, in an iterator over components[*], to access the parent with a relative path, for example:

However, this is not standardized and depends on the engine.

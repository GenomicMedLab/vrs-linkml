# general

* no special `const` property (though attainable via regex for string values).
* no `default` property. I think this makes sense, and could be implemented as a default or option for const values in external code generators.
* no min/max # in arrays

# gen pydantic/etc

* inheritance -- seems like classes redefine inherited values explicitly rather than just inheriting them
* abstract class -- doesn't get represented in pydantic
* should think about doc generation. Right now we include lil RST hyperlinks in the descriptions, that might be somehow adjustable so they get removed in pydantic.
* not sure how to provide a list of types to a range
    * also not sure how to make array/list one of those types
* required = true seems inconsistent?
* pattern isn't propogated -- should be `regex` arg in `Field()`

.PHONY: pydantic

pydantic: src/vrs.yaml
ifeq ($(stacktrace),1)
	gen-pydantic --stacktrace src/vrs.yaml > generated/vrs.py
else
	gen-pydantic src/vrs.yaml > generated/vrs.py
endif
	black --quiet generated/vrs.py



.PHONY: jsonschema

jsonschema: src/vrs.yaml
	gen-json-schema src/vrs.yaml > generated/vrs.json
	prettier -w generated/vrs.json

.PHONY: markdown

markdown: src/vrs.yaml
	gen-markdown --index-file docs/schema.md -d docs src/vrs.yaml

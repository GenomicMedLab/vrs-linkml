.PHONY: pydantic

pydantic: src/gks_core.yaml
	gen-pydantic src/gks_core.yaml > generated/gks_core.py
	black --quiet generated/gks_core.py

jsonschema: src/gks_core.yaml
	gen-json-schema src/gks_core.yaml > generated/gks_core.json
	prettier -w generated/gks_core.json

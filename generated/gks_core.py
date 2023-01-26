from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel as BaseModel, Field
from linkml_runtime.linkml_model import Decimal

metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(
    WeakRefShimBaseModel,
    validate_assignment=True,
    validate_all=True,
    underscore_attrs_are_private=True,
    extra="forbid",
    arbitrary_types_allowed=True,
):
    pass


class Entity(ConfiguredBaseModel):
    """
    Entity is the root class of ‘core’ classes model - those that have identifiers and other general metadata like labels, xrefs, urls, descriptions, etc. All core classes descend from and inherit its attributes.
    """

    id: Optional[str] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, e.g. a UUID. This 'id' is unique within a given system. The identified entity may have a different 'id' in a different system, or may refer to an 'id' for the shared concept in another system (e.g. a CURIE).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class ValueEntity(Entity):
    """
    ValueEntity is the root class for classes that instantiate Value Objects. ValueEntity classes are not extensible and MUST NOT have optional properties.
    """

    id: Optional[str] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class DomainEntity(ValueEntity):
    """
    An abstract :ref:`ValueEntity` class extended to capture specific domain entities by reference to an external identifier.
    """

    id: str = Field(None)
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class ExtensibleEntity(Entity):
    """
    ExtensibleEntity is the root class for classes that instantiate Extensible Objects. Extensible Objects are extensible using the extensions property and MAY have optional properties.
    """

    label: Optional[str] = Field(None)
    extensions: Optional[List[Extension]] = Field(default_factory=list)
    id: Optional[str] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, e.g. a UUID. This 'id' is unique within a given system. The identified entity may have a different 'id' in a different system, or may refer to an 'id' for the shared concept in another system (e.g. a CURIE).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class Extension(ConfiguredBaseModel):
    """
    The Extension class provides VODs with a means to extend descriptions with other attributes unique to a content provider. These extensions are not expected to be natively understood under VRSATILE, but may be used for pre-negotiated exchange of message attributes when needed.
    """

    type: str = Field(None)
    name: str = Field(None, description="""A name for the Extension""")
    value: Optional[str] = Field(
        None, description="""Any primitive or structured object"""
    )


class RecordMetadata(ExtensibleEntity):
    """
    A re-usable structure that encapsulates provenance metadata that applies to a specific concrete record of information as encoded in a particular system, as opposed to provenance of the abstract information content/knowledge the record represents.
    """

    type: str = Field(None)
    is_version_of: Optional[str] = Field(None)
    version: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    extensions: Optional[List[Extension]] = Field(default_factory=list)
    id: Optional[str] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, e.g. a UUID. This 'id' is unique within a given system. The identified entity may have a different 'id' in a different system, or may refer to an 'id' for the shared concept in another system (e.g. a CURIE).""",
    )


class Coding(ExtensibleEntity):
    """
    A `coding` is an extensible entity for labeling or otherwise annotating globally namespaced identifiers known as \"codes\".
    """

    type: str = Field(None)
    id: Optional[str] = Field(
        None,
        description="""The `coding.id` field is used to capture the code as a CURIE.""",
    )
    record_metadata: Optional[RecordMetadata] = Field(None)
    label: Optional[str] = Field(None)
    extensions: Optional[List[Extension]] = Field(default_factory=list)


class Disease(DomainEntity):
    """
    A reference to a Disease as defined by an authority. For human diseases, the use of `MONDO <https://registry.identifiers.org/registry/mondo>`_ as the disease authority is RECOMMENDED.
    """

    type: str = Field(None)
    id: str = Field(None)


class Phenotype(DomainEntity):
    """
    A reference to a Phenotype as defined by an authority. For human phenotypes, the use of `HPO <https://registry.identifiers.org/registry/hpo>`_ as the disease authority is RECOMMENDED.
    """

    type: str = Field(None)
    id: str = Field(None)


class Gene(DomainEntity):
    """
    A reference to a Gene as defined by an authority. For human genes, the use of `hgnc <https://registry.identifiers.org/registry/hgnc>`_ as the gene authority is RECOMMENDED.
    """

    type: str = Field(None)
    id: str = Field(None)


class Condition(ValueEntity):
    """
    A set of phenotype and/or disease concepts that constitute a condition.
    """

    members: List[Disease] = Field(default_factory=list)
    id: Optional[str] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class Therapeutic(DomainEntity):
    """
    A treatment, therapy, or drug.
    """

    type: str = Field(None)
    id: str = Field(None)


class TherapeuticCollection(ValueEntity):
    """
    A collection of therapeutics.
    """

    members: List[Disease] = Field(default_factory=list)
    id: Optional[str] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class CombinationTherapeuticCollection(TherapeuticCollection):
    """
    A collection of therapeutics that are taken during a course of treatment.
    """

    type: str = Field(None)
    members: List[Disease] = Field(default_factory=list)
    id: Optional[str] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class SubstituteTherapeuticCollection(TherapeuticCollection):
    """
    A collection of therapeutics that are considered as valid alternative entities.
    """

    type: str = Field(None)
    members: List[Disease] = Field(default_factory=list)
    id: Optional[str] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Entity.update_forward_refs()
ValueEntity.update_forward_refs()
DomainEntity.update_forward_refs()
ExtensibleEntity.update_forward_refs()
Extension.update_forward_refs()
RecordMetadata.update_forward_refs()
Coding.update_forward_refs()
Disease.update_forward_refs()
Phenotype.update_forward_refs()
Gene.update_forward_refs()
Condition.update_forward_refs()
Therapeutic.update_forward_refs()
TherapeuticCollection.update_forward_refs()
CombinationTherapeuticCollection.update_forward_refs()
SubstituteTherapeuticCollection.update_forward_refs()

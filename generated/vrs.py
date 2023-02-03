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


class SequenceExpression(ConfiguredBaseModel):
    """
    An expression describing a :ref:`Sequence`.
    """

    None


class LiteralSequenceExpression(SequenceExpression):
    """
    An explicit expression of a Sequence.
    """

    type: str = Field(None)
    sequence: string = Field(
        None, description="""the literal :ref:`Sequence` expressed"""
    )


class DerivedSequenceExpression(SequenceExpression):
    """
    An approximate expression of a sequence that is derived from a referenced sequence location. Use of this class indicates that the derived sequence is *approximately equivalent* to the reference indicated, and is typically used for describing large regions in contexts where the use of an approximate sequence is inconsequential.
    """

    type: Optional[str] = Field(None)
    location: string = Field(
        None,
        description="""The location from which the approximate sequence is derived""",
    )
    reverse_complement: bool = Field(
        None,
        description="""A flag indicating if the expressed sequence is the reverse complement of the sequence referred to by `location`""",
    )


class RepeatedSequenceExpression(SequenceExpression):
    """
    An expression of a sequence comprised of a tandem repeating subsequence.
    """

    type: Optional[str] = Field(None)
    seq_expr: LiteralSequenceExpression = Field(
        None, description="""An expression of the repeating subsequence"""
    )
    count: Number = Field(
        None,
        description="""The count of repeated units, as an integer or inclusive range""",
    )


class ComposedSequenceExpression(ConfiguredBaseModel):
    """
    An expression of a sequence composed from multiple other :ref:`Sequence Expressions<SequenceExpression>` objects. MUST have at least one component that is not a ref:`LiteralSequenceExpression`. CANNOT be composed from nested composed sequence expressions.
    """

    type: Optional[str] = Field(None)
    components: List[LiteralSequenceExpression] = Field(
        default_factory=list,
        description="""An ordered list of :ref:`SequenceExpression` components comprising the expression. MUST NOT have two adjacent :ref:`LiteralSequenceExpression` objects.""",
    )


class GenotypeMember(ConfiguredBaseModel):
    """
    A class for expressing the count of a specific :ref:`MolecularVariation` present _in-trans_ at a genomic locus represented by a :ref:`Genotype`.
    """

    type: Optional[str] = Field(None)
    count: Number = Field(
        None,
        description="""The number of copies of the `variation` at a :ref:`Genotype` locus.""",
    )
    variation: Allele = Field(
        None, description="""A :ref:`MolecularVariation` at a :ref:`Genotype` locus."""
    )


class Number(ConfiguredBaseModel):
    """
    A simple integer value as a VRS class.
    """

    type: str = Field(None)
    value: int = Field(None, description="""The value represented by Number""")


class DefiniteRange(ConfiguredBaseModel):
    """
    A bounded, inclusive range of numbers.
    """

    type: str = Field(None)
    min: Number = Field(None, description="""The minimum value; inclusive""")
    max: Number = Field(None, description="""The maximum value; inclusive""")


class IndefiniteRange(ConfiguredBaseModel):
    """
    A half-bounded range of numbers represented as a number bound and associated comparator. The bound operator is interpreted as follows: '>=' are all numbers greater than and including `value`, '<=' are all numbers less than and including `value`.
    """

    type: str = Field(None)
    value: int = Field(None, description="""The bounded value; inclusive""")
    comparator: str = Field(
        None,
        description="""MUST be one of \"<=\" or \">=\", indicating which direction the range is indefinite""",
    )


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

    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class Variation(ValueEntity):
    """
    A representation of the state of one or more biomolecules.
    """

    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class MolecularVariation(Variation):
    """
    A :ref:`variation` on a contiguous molecule.
    """

    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class UtilityVariation(Variation):
    """
    A collection of :ref:`Variation` subclasses that cannot be constrained to a specific class of biological variation, but are necessary for some applications of VRS.
    """

    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class SystemicVariation(Variation):
    """
    A Variation of multiple molecules in the context of a system, e.g. a genome, sample, or homologous chromosomes.
    """

    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class Allele(MolecularVariation):
    """
    The state of a molecule at a :ref:`Location`.
    """

    type: Optional[str] = Field(None)
    location: string = Field(
        None, description="""An expression of the sequence state."""
    )
    state: SequenceExpression = Field(
        None, description="""An expression of the sequence state"""
    )
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class Haplotype(MolecularVariation):
    """
    A set of non-overlapping :ref:`Allele` members that co-occur on the same molecule.
    """

    type: Optional[str] = Field(None)
    members: List[string] = Field(
        default_factory=list,
        description="""List of Alleles, or references to Alleles, that comprise this Haplotype.""",
    )
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class Text(UtilityVariation):
    """
    A free-text definition of variation.
    """

    type: Optional[str] = Field(None)
    definition: str = Field(
        None,
        description="""A textual representation of variation not representable by other subclasses of Variation.""",
    )
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class VariationSet(UtilityVariation):
    """
    An unconstrained set of Variation members.
    """

    type: Optional[str] = Field(None)
    members: List[string] = Field(
        default_factory=list,
        description="""List of Variation objects or identifiers. Attribute is required, but MAY be empty.""",
    )
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class CopyNumber(SystemicVariation):
    """
    A measure of the copies of a :ref:`Location` within a system (e.g. a genome)
    """

    location: string = Field(None, description="""The location within the system.""")
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class AbsoluteCopyNumber(CopyNumber):
    """
    The absolute count of discrete copies of a :ref:`MolecularVariation`, :ref:`Feature`, :ref:`SequenceExpression`, or a :ref:`CURIE` reference within a system (e.g. genome, cell, etc.).
    """

    type: Optional[str] = Field(None)
    copies: Number = Field(
        None,
        description="""The integral number of copies of the subject in a system.""",
    )
    location: string = Field(None, description="""The location within the system.""")
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class RelativeCopyNumber(CopyNumber):
    """
    The relative copies of a :ref:`MolecularVariation`, :ref:`Feature`, :ref:`SequenceExpression`, or a :ref:`CURIE` reference against an unspecified baseline in a system (e.g. genome, cell, etc.).
    """

    type: Optional[str] = Field(None)
    relative_copy_class: str = Field(
        None,
        description="""MUST be one of \"EFO:0030070\", \"EFO:0030072\", \"EFO:0030071\", \"EFO:0030067\", \"EFO:0030069\", or \"EFO:0030068\".""",
    )
    location: string = Field(None, description="""The location within the system.""")
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class Genotype(SystemicVariation):
    """
    A quantified set of _in-trans_ :ref:`MolecularVariation` at a genomic locus.
    """

    type: Optional[str] = Field(None)
    members: List[string] = Field(
        default_factory=list,
        description="""Each GenotypeMember in `members` describes a :ref:`MolecularVariation` and the count of that variation at the locus.""",
    )
    count: Number = Field(
        None,
        description="""The total number of copies of all :ref:`MolecularVariation` at this locus, MUST be greater than or equal to the sum of :ref:`GenotypeMember` copy counts. If greater than the total counts, this implies additional :ref:`MolecularVariation` that are expected to exist but are not explicitly indicated.""",
    )
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class Location(ValueEntity):
    """
    A contiguous segment of a biological sequence.
    """

    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )
    type: str = Field(
        None,
        description="""The schema class that is instantiated by the data object. Must be the name of a class from the VA schema.""",
    )


class ChromosomeLocation(Location):
    """
    A Location on a chromosome defined by a species and chromosome name.
    """

    type: Optional[str] = Field(None)
    species_id: string = Field(
        None,
        description=""":ref:`CURIE` representing a species from the `NCBI species taxonomy <https://registry.identifiers.org/registry/taxonomy>`_. Default: \"taxonomy:9606\" (human)""",
    )
    chr: str = Field(
        None,
        description="""The symbolic chromosome name. For humans, For humans, chromosome names MUST be one of 1..22, X, Y (case-sensitive)""",
    )
    start: string = Field(
        None,
        description="""The start cytoband region. MUST specify a region nearer the terminal end (telomere) of the chromosome p-arm than `end`.""",
    )
    end: string = Field(
        None,
        description="""The start cytoband region. MUST specify a region nearer the terminal end (telomere) of the chromosome q-arm than `start`.""",
    )
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class SequenceLocation(Location):
    """
    A :ref:`Location` defined by an interval on a referenced :ref:`Sequence`.
    """

    type: Optional[str] = Field(None)
    sequence_id: string = Field(
        None,
        description="""A VRS :ref:`Computed Identifier <computed-identifiers>` for the reference :ref:`Sequence`.""",
    )
    start: string = Field(
        None,
        description="""The start coordinate or range of the SequenceLocation. The minimum value of this coordinate or range is 0. MUST represent a coordinate or range less than the value of `end`.""",
    )
    end: string = Field(
        None,
        description="""The end coordinate or range of the SequenceLocation. The minimum value of this coordinate or range is 0. MUST represent a coordinate or range greater than the value of `start`.""",
    )
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
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

    type: Optional[str] = Field(None)
    name: str = Field(None, description="""A name for the Extension""")
    value: int = Field(None, description="""Any primitive or structured object""")


class RecordMetadata(ExtensibleEntity):
    """
    A re-usable structure that encapsulates provenance metadata that applies to a specific concrete record of information as encoded in a particular system, as opposed to provenance of the abstract information content/knowledge the record represents.
    """

    type: Optional[str] = Field(None)
    is_version_of: Optional[string] = Field(None)
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

    type: Optional[str] = Field(None)
    id: Optional[string] = Field(
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

    type: Optional[str] = Field(None)
    id: str = Field(None)


class Phenotype(DomainEntity):
    """
    A reference to a Phenotype as defined by an authority. For human phenotypes, the use of `HPO <https://registry.identifiers.org/registry/hpo>`_ as the disease authority is RECOMMENDED.
    """

    type: Optional[str] = Field(None)
    id: str = Field(None)


class Gene(DomainEntity):
    """
    A reference to a Gene as defined by an authority. For human genes, the use of `hgnc <https://registry.identifiers.org/registry/hgnc>`_ as the gene authority is RECOMMENDED.
    """

    type: Optional[str] = Field(None)
    id: str = Field(None)


class Condition(ValueEntity):
    """
    A set of phenotype and/or disease concepts that constitute a condition.
    """

    members: List[string] = Field(default_factory=list)
    id: Optional[string] = Field(
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

    type: Optional[str] = Field(None)
    id: str = Field(None)


class TherapeuticCollection(ValueEntity):
    """
    A collection of therapeutics.
    """

    members: List[string] = Field(default_factory=list)
    id: Optional[string] = Field(
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

    type: Optional[str] = Field(None)
    members: List[string] = Field(default_factory=list)
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


class SubstituteTherapeuticCollection(TherapeuticCollection):
    """
    A collection of therapeutics that are considered as valid alternative entities.
    """

    type: Optional[str] = Field(None)
    members: List[string] = Field(default_factory=list)
    id: Optional[string] = Field(
        None,
        description="""The 'logical' identifier of the entity in the system of record, and MUST be represented as a CURIE. This 'id' is unique within a given system, but may also refer to an 'id' for the shared concept in another system (represented by namespace, accordingly).""",
    )


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
SequenceExpression.update_forward_refs()
LiteralSequenceExpression.update_forward_refs()
DerivedSequenceExpression.update_forward_refs()
RepeatedSequenceExpression.update_forward_refs()
ComposedSequenceExpression.update_forward_refs()
GenotypeMember.update_forward_refs()
Number.update_forward_refs()
DefiniteRange.update_forward_refs()
IndefiniteRange.update_forward_refs()
Entity.update_forward_refs()
ValueEntity.update_forward_refs()
Variation.update_forward_refs()
MolecularVariation.update_forward_refs()
UtilityVariation.update_forward_refs()
SystemicVariation.update_forward_refs()
Allele.update_forward_refs()
Haplotype.update_forward_refs()
Text.update_forward_refs()
VariationSet.update_forward_refs()
CopyNumber.update_forward_refs()
AbsoluteCopyNumber.update_forward_refs()
RelativeCopyNumber.update_forward_refs()
Genotype.update_forward_refs()
Location.update_forward_refs()
ChromosomeLocation.update_forward_refs()
SequenceLocation.update_forward_refs()
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

# Auto generated from edge.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-03-10 14:31
# Schema: Monarch-Solr-Edge
#
# id: https://w3id.org/monarch/monarch-solr-edge
# description: Edge/Association data model for Monarch Solr
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://w3id.org/monarch/monarch-solr-edge/')


# Types

# Class references
class EdgeId(extended_str):
    pass


@dataclass
class Edge(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://w3id.org/monarch/monarch-solr-edge/Edge")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "edge"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/monarch/monarch-solr-edge/Edge")

    id: Union[str, EdgeId] = None
    category: Optional[str] = None
    subject: Optional[str] = None
    subject_closure: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    object_closure: Optional[str] = None
    relation: Optional[str] = None
    provided_by: Optional[str] = None
    knowledge_source: Optional[str] = None
    publications: Optional[str] = None
    qualifiers: Optional[str] = None
    source: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EdgeId):
            self.id = EdgeId(self.id)

        if self.category is not None and not isinstance(self.category, str):
            self.category = str(self.category)

        if self.subject is not None and not isinstance(self.subject, str):
            self.subject = str(self.subject)

        if self.subject_closure is not None and not isinstance(self.subject_closure, str):
            self.subject_closure = str(self.subject_closure)

        if self.predicate is not None and not isinstance(self.predicate, str):
            self.predicate = str(self.predicate)

        if self.object is not None and not isinstance(self.object, str):
            self.object = str(self.object)

        if self.object_closure is not None and not isinstance(self.object_closure, str):
            self.object_closure = str(self.object_closure)

        if self.relation is not None and not isinstance(self.relation, str):
            self.relation = str(self.relation)

        if self.provided_by is not None and not isinstance(self.provided_by, str):
            self.provided_by = str(self.provided_by)

        if self.knowledge_source is not None and not isinstance(self.knowledge_source, str):
            self.knowledge_source = str(self.knowledge_source)

        if self.publications is not None and not isinstance(self.publications, str):
            self.publications = str(self.publications)

        if self.qualifiers is not None and not isinstance(self.qualifiers, str):
            self.qualifiers = str(self.qualifiers)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.subject = Slot(uri=DEFAULT_.subject, name="subject", curie=DEFAULT_.curie('subject'),
                   model_uri=DEFAULT_.subject, domain=None, range=Optional[str])

slots.predicate = Slot(uri=DEFAULT_.predicate, name="predicate", curie=DEFAULT_.curie('predicate'),
                   model_uri=DEFAULT_.predicate, domain=None, range=Optional[str])

slots.object = Slot(uri=DEFAULT_.object, name="object", curie=DEFAULT_.curie('object'),
                   model_uri=DEFAULT_.object, domain=None, range=Optional[str])

slots.category = Slot(uri=DEFAULT_.category, name="category", curie=DEFAULT_.curie('category'),
                   model_uri=DEFAULT_.category, domain=None, range=Optional[str])

slots.relation = Slot(uri=DEFAULT_.relation, name="relation", curie=DEFAULT_.curie('relation'),
                   model_uri=DEFAULT_.relation, domain=None, range=Optional[str])

slots.provided_by = Slot(uri=DEFAULT_.provided_by, name="provided_by", curie=DEFAULT_.curie('provided_by'),
                   model_uri=DEFAULT_.provided_by, domain=None, range=Optional[str])

slots.knowledge_source = Slot(uri=DEFAULT_.knowledge_source, name="knowledge_source", curie=DEFAULT_.curie('knowledge_source'),
                   model_uri=DEFAULT_.knowledge_source, domain=None, range=Optional[str])

slots.publications = Slot(uri=DEFAULT_.publications, name="publications", curie=DEFAULT_.curie('publications'),
                   model_uri=DEFAULT_.publications, domain=None, range=Optional[str])

slots.qualifiers = Slot(uri=DEFAULT_.qualifiers, name="qualifiers", curie=DEFAULT_.curie('qualifiers'),
                   model_uri=DEFAULT_.qualifiers, domain=None, range=Optional[str])

slots.source = Slot(uri=DEFAULT_.source, name="source", curie=DEFAULT_.curie('source'),
                   model_uri=DEFAULT_.source, domain=None, range=Optional[str])

slots.subject_closure = Slot(uri=DEFAULT_.subject_closure, name="subject_closure", curie=DEFAULT_.curie('subject_closure'),
                   model_uri=DEFAULT_.subject_closure, domain=None, range=Optional[str])

slots.object_closure = Slot(uri=DEFAULT_.object_closure, name="object_closure", curie=DEFAULT_.curie('object_closure'),
                   model_uri=DEFAULT_.object_closure, domain=None, range=Optional[str])

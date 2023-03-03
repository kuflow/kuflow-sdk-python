from typing import Any, Optional, Type
import json

from temporalio import workflow
from temporalio.api.common.v1 import Payload
from temporalio.converter import (
    CompositePayloadConverter,
    DefaultPayloadConverter,
    EncodingPayloadConverter,
    JSONPlainPayloadConverter,
)

from kuflow_rest import models as models_rest

from . import models as models_temporal

with workflow.unsafe.imports_passed_through():
    from kuflow_rest import Serializer, Deserializer, Model


class KuFlowEncodingPayloadConverter(EncodingPayloadConverter):
    _default_json_converter: JSONPlainPayloadConverter

    _serialize: Serializer
    _deserialize: Deserializer

    def __init__(self, default_json_converter=JSONPlainPayloadConverter()) -> None:
        self._default_json_converter = default_json_converter
        client_models_rest = {k: v for k, v in models_rest.__dict__.items() if isinstance(v, type)}
        client_models_temporal = {k: v for k, v in models_temporal.__dict__.items() if isinstance(v, type)}
        client_models = {**client_models_rest, **client_models_temporal}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

    @property
    def encoding(self) -> str:
        return "json/plain"

    def to_payload(self, value: Any) -> Optional[Payload]:
        if isinstance(value, Model):
            serialized = self._serialize.body(value, value.__class__.__name__)
            return self._default_json_converter.to_payload(serialized)
        else:
            return self._default_json_converter.to_payload(value)

    def from_payload(self, payload: Payload, type_hint: Optional[Type] = None) -> Any:
        # Only supports json/plain. You need to modify this converter in order tu support encryption
        message_type = payload.metadata.get("encoding", b"<unknown>").decode()
        if message_type != "json/plain":
            return self._default_json_converter.from_payload(payload.data, type_hint)

        if issubclass(type_hint, Model):
            as_python_object = json.loads(payload.data)
            return self._deserialize(type_hint.__name__, as_python_object)
        else:
            return self._default_json_converter.from_payload(payload, type_hint)


class KuFlowPayloadConverter(CompositePayloadConverter):
    def __init__(self) -> None:
        #  Replace default JSONPlainPayloadConverter with a custom converter for KuFlow
        super().__init__(
            *[
                c if not isinstance(c, JSONPlainPayloadConverter) else KuFlowEncodingPayloadConverter()
                for c in DefaultPayloadConverter.default_encoding_payload_converters
            ]
        )

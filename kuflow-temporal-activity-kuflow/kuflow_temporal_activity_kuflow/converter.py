#
# MIT License
#
# Copyright (c) 2022 KuFlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
from typing import Any, Optional, Type

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
    from kuflow_rest import Deserializer, Model, Serializer


class KuFlowComposableEncodingPayloadConverter(EncodingPayloadConverter):
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
        if isinstance(value, Model) is False:
            return None

        serialized = self._serialize.body(value, value.__class__.__name__)
        return self._default_json_converter.to_payload(serialized)

    def from_payload(self, payload: Payload, type_hint: Optional[Type] = None) -> Any:
        if issubclass(type_hint, Model) is False:
            return None

        as_python_object = json.loads(payload.data)
        return self._deserialize(type_hint.__name__, as_python_object)


class KuFlowEncodingPayloadConverter(EncodingPayloadConverter):
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

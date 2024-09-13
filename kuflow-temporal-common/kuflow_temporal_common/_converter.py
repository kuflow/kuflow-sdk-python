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
from typing import Any, Dict, List, Optional, Type

from temporalio.api.common.v1 import Payload
from temporalio.converter import (
    EncodingPayloadConverter,
    JSONPlainPayloadConverter,
)

from kuflow_rest import Deserializer, Model, Serializer


temporal_models: Dict[str, type] = {}


def register_serializable_models(models: Dict[str, type]):
    global temporal_models

    temporal_models_tmp = {k: v for k, v in models.items() if isinstance(v, type)}
    temporal_models_tmp = {**temporal_models, **temporal_models_tmp}
    temporal_models = temporal_models_tmp


class CompositeEncodingPayloadConverter(EncodingPayloadConverter):
    """Composite encoding payload converter that delegates to a list of encoding payload converters.

    Encoding/decoding are attempted on each payload converter successively until
    it succeeds.

    """

    def __init__(self, encoding: str, converters: List[EncodingPayloadConverter]):
        """Initializes the encoding data converter.

        Arguments:
            encoding: Encoding of this EncodingPayloadConverter
            converters: Encoding payload converters to delegate to, in order.
        """
        self.register_encoding = encoding
        self.converters = converters

    @property
    def encoding(self) -> str:
        return self.register_encoding

    def to_payload(self, value: Any) -> Optional[Payload]:
        payload: Optional[Payload] = None
        for converter in self.converters:
            payload = converter.to_payload(value)
            if payload is not None:
                break

        return payload

    def from_payload(self, payload: Payload, type_hint: Optional[Type] = None) -> Any:
        value: Optional[Payload] = None
        for converter in self.converters:
            value = converter.from_payload(payload, type_hint)
            if value is not None:
                break

        return value


class KuFlowComposableEncodingPayloadConverter(EncodingPayloadConverter):
    def __init__(self, default_json_converter=JSONPlainPayloadConverter()) -> None:
        self._default_json_converter = default_json_converter
        client_models = {k: v for k, v in temporal_models.items() if isinstance(v, type)}
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

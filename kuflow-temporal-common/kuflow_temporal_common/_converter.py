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

from typing import Any, Optional, Union

from temporalio.converter import (
    AdvancedJSONEncoder,
    JSONTypeConverter,
    _JSONTypeConverterUnhandled,
)

from kuflow_rest import Deserializer, Model, Serializer


temporal_models: dict[str, type] = {}


def register_serializable_models(models: dict[str, type]):
    global temporal_models

    temporal_models_tmp = {k: v for k, v in models.items() if isinstance(v, type)}
    temporal_models_tmp = {**temporal_models, **temporal_models_tmp}
    temporal_models = temporal_models_tmp


class KuFlowModelJSONEncoder(AdvancedJSONEncoder):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        client_models = {k: v for k, v in temporal_models.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)

    def default(self, value: Any) -> Any:
        if isinstance(value, Model):
            return self._serialize.body(value, value.__class__.__name__)

        return super().default(value)


class KuFlowModelJSONTypeConverter(JSONTypeConverter):
    def __init__(self) -> None:
        client_models = {k: v for k, v in temporal_models.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)

    def to_typed_value(self, hint: type, value: Any) -> Union[Optional[Any], _JSONTypeConverterUnhandled]:
        if issubclass(hint, Model):
            return self._deserialize(hint.__name__, value)

        return JSONTypeConverter.Unhandled

from typing import Any, List, Optional, Type, Union

from temporalio.api.common.v1 import Payload
from temporalio.converter import EncodingPayloadConverter
from temporalio.types import CallableType, ClassType


def register(
    cls_or_fn: Optional[Union[CallableType, ClassType]] = None,
    encoding_payload_converter_class: Optional[Type[EncodingPayloadConverter]] = None,
):
    """A decorator to annotate that this temporal workflow or activity method needs a converter class.

    Usage:
        @workflow.defn(name="SampleWorkflow")
        @converter.register_for_workflow(encoding_payload_converter_class=CustomEncodingPayloadConverter)
        class SampleWorkflow:
            ...

        OR

        @converter.register_for_activity(encoding_payload_converter_class=CustomEncodingPayloadConverter)
        def activity_method(self, ...):
            ...
    """

    def decorator(_cls_or_fn: CallableType) -> CallableType:
        _cls_or_fn.__kuflow_encoding_payload_converter_class__ = encoding_payload_converter_class

        return _cls_or_fn

    if cls_or_fn is not None:
        return decorator(cls_or_fn)
    return decorator


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

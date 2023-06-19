from typing import Any, Optional, Type, List

from temporalio.api.common.v1 import Payload
from temporalio.converter import EncodingPayloadConverter
from temporalio.types import CallableType


def register(
    fn: Optional[CallableType] = None, encoding_payload_converter_class: Optional[Type[EncodingPayloadConverter]] = None
):
    """A decorator to annotate that this temporal method needs a converter class.

    Usage:
            @kuflow_temporal_converter(encoding_payload_converter_class=CustomEncodingPayloadConverter)
            def activity_method(self, ...):
                ...
    """
    fn.__kuflow_encoding_payload_converter_class__ = encoding_payload_converter_class

    return fn


class CompositeEncodingPayloadConverter(EncodingPayloadConverter):
    """Composite encoding payload converter that delegates to a list of encoding payload converters.

    Encoding/decoding are attempted on each payload converter successively until
    it succeeds.

    Attributes:
        register_encoding: Encoding of this EncodingPayloadConverter
        converters: List of payload converters to delegate to, in order.
    """

    register_encoding: str

    converters: List[EncodingPayloadConverter]

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

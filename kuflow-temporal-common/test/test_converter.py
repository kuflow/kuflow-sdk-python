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
from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

import pytest
from temporalio.converter import JSONPlainPayloadConverter

from kuflow_rest import Model
from kuflow_rest import models as models_rest
from kuflow_temporal_common._converter import (
    KuFlowModelJSONEncoder,
    KuFlowModelJSONTypeConverter,
    register_serializable_models,
)


class SampleEnum(StrEnum):
    VALUE_ONE = "value_one"
    VALUE_TWO = "value_two"


class TestConverterRoundTrip:
    """Test encoding and decoding round-trip using JSONPlainPayloadConverter"""

    @pytest.fixture
    def converter(self):
        return JSONPlainPayloadConverter(
            encoder=KuFlowModelJSONEncoder,
            custom_type_converters=[KuFlowModelJSONTypeConverter()],
        )

    def test_uuid_roundtrip(self, converter):
        """Test UUID serialization and deserialization"""
        original = UUID("12345678-1234-5678-1234-567812345678")

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, UUID)

        assert result == original

    def test_bytes_roundtrip(self, converter):
        """Test bytes serialization and deserialization"""
        original = b"Hello, World!"

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, bytes)

        assert result == original

    def test_enum_roundtrip(self, converter):
        """Test Enum serialization and deserialization"""
        original = SampleEnum.VALUE_ONE

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, SampleEnum)

        assert result == original

    def test_none_roundtrip(self, converter):
        """Test None serialization and deserialization"""
        original = None

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, Optional[str])

        assert result is None

    def test_list_of_uuid_roundtrip(self, converter):
        """Test list[UUID] serialization and deserialization"""
        original = [
            UUID("12345678-1234-5678-1234-567812345678"),
            UUID("87654321-4321-8765-4321-876543218765"),
        ]

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, list[UUID])

        assert result == original

    def test_dict_of_str_to_uuid_roundtrip(self, converter):
        """Test dict[str, UUID] serialization and deserialization"""
        original = {
            "id1": UUID("12345678-1234-5678-1234-567812345678"),
            "id2": UUID("87654321-4321-8765-4321-876543218765"),
        }

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, dict[str, UUID])

        assert result == original

    def test_optional_datetime_with_none_roundtrip(self, converter):
        """Test Optional[datetime] with None serialization and deserialization"""
        original = None

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, Optional[datetime])

        assert result is None


class TestEncoderOnly:
    """Test encoder-specific functionality"""

    def test_encoder_uuid(self):
        """Test UUID encoding to string"""
        uuid_obj = UUID("12345678-1234-5678-1234-567812345678")

        result = json.dumps(uuid_obj, cls=KuFlowModelJSONEncoder)

        assert result == f'"{str(uuid_obj)}"'

    def test_encoder_enum(self):
        """Test Enum encoding to value"""
        enum_val = SampleEnum.VALUE_ONE

        result = json.dumps(enum_val, cls=KuFlowModelJSONEncoder)

        assert result == f'"{enum_val.value}"'

    pass  # Keep class with at least one statement


class TestKuFlowModelRoundTrip:
    """Regression test: a real KuFlow REST Model must survive the Temporal round-trip.

    This guards against the serialization module being re-exported from a stale/duplicate
    location (e.g. AutoRest relocating `_serialization` to `_utils/serialization`), which
    would make ``isinstance(value, Model)`` False for every KuFlow model and silently break
    payload conversion across the workflow/activity boundary.
    """

    @pytest.fixture(autouse=True)
    def _register_models(self):
        # Models must be registered before the converter is constructed (it captures them in __init__).
        register_serializable_models(models_rest.__dict__)

    @pytest.fixture
    def converter(self):
        return JSONPlainPayloadConverter(
            encoder=KuFlowModelJSONEncoder,
            custom_type_converters=[KuFlowModelJSONTypeConverter()],
        )

    def test_kuflow_model_is_recognized(self):
        """The public Model class must be the one KuFlow REST models actually subclass."""
        process = self._build_process()

        assert isinstance(process, Model)

    def test_process_model_roundtrip(self, converter):
        """A Process must serialize and deserialize back to an equivalent Process."""
        original = self._build_process()

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, models_rest.Process)

        assert isinstance(result, models_rest.Process)
        assert str(result.id) == str(original.id)
        assert str(result.tenant_id) == str(original.tenant_id)
        assert str(result.state) == str(original.state)
        assert str(result.process_definition_ref.id) == str(original.process_definition_ref.id)

    @staticmethod
    def _build_process() -> "models_rest.Process":
        process_definition_ref = models_rest.ProcessDefinitionRef(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            version=UUID("87654321-4321-8765-4321-876543218765"),
            code="PROCESS_DEFINITION_CODE",
        )
        return models_rest.Process(
            id=UUID("11111111-1111-1111-1111-111111111111"),
            tenant_id=UUID("22222222-2222-2222-2222-222222222222"),
            process_definition_ref=process_definition_ref,
            state="RUNNING",
        )

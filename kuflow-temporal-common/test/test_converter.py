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

import base64
import json
from datetime import date, datetime, time, timedelta
from enum import StrEnum
from typing import Optional
from uuid import UUID

import pytest
from temporalio.converter import JSONPlainPayloadConverter, value_to_type

from kuflow_temporal_common._converter import KuFlowModelJSONEncoder, KuFlowModelJSONTypeConverter


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

    # def test_datetime_roundtrip(self, converter):
    #     """Test datetime serialization and deserialization"""
    #     original = datetime(2025, 11, 19, 15, 30, 45, 123456)

    #     # Encode
    #     payload = converter.to_payload(original)

    #     # Decode
    #     result = converter.from_payload(payload, datetime)

    #     assert result == original

    # def test_date_roundtrip(self, converter):
    #     """Test date serialization and deserialization"""
    #     original = date(2025, 11, 19)

    #     payload = converter.to_payload(original)
    #     result = converter.from_payload(payload, date)

    #     assert result == original

    # def test_time_roundtrip(self, converter):
    #     """Test time serialization and deserialization"""
    #     original = time(15, 30, 45, 123456)

    #     payload = converter.to_payload(original)
    #     result = converter.from_payload(payload, time)

    #     assert result == original

    # def test_timedelta_roundtrip(self, converter):
    #     """Test timedelta serialization and deserialization"""
    #     original = timedelta(days=5, hours=3, minutes=30, seconds=45)

    #     payload = converter.to_payload(original)
    #     result = converter.from_payload(payload, timedelta)

    #     assert result == original

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

    # def test_bytearray_roundtrip(self, converter):
    #     """Test bytearray serialization and deserialization"""
    #     original = bytearray(b"Hello, World!")

    #     payload = converter.to_payload(original)
    #     result = converter.from_payload(payload, bytearray)

    #     assert result == original

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

    # def test_list_of_datetime_roundtrip(self, converter):
    #     """Test list[datetime] serialization and deserialization"""
    #     original = [
    #         datetime(2025, 11, 19, 15, 30, 45),
    #         datetime(2025, 11, 20, 10, 15, 30),
    #     ]

    #     payload = converter.to_payload(original)
    #     result = converter.from_payload(payload, list[datetime])

    #     assert result == original

    def test_list_of_uuid_roundtrip(self, converter):
        """Test list[UUID] serialization and deserialization"""
        original = [
            UUID("12345678-1234-5678-1234-567812345678"),
            UUID("87654321-4321-8765-4321-876543218765"),
        ]

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, list[UUID])

        assert result == original

    # def test_dict_of_str_to_datetime_roundtrip(self, converter):
    #     """Test dict[str, datetime] serialization and deserialization"""
    #     original = {
    #         "created": datetime(2025, 11, 19, 15, 30, 45),
    #         "modified": datetime(2025, 11, 20, 10, 15, 30),
    #     }

    #     payload = converter.to_payload(original)
    #     result = converter.from_payload(payload, dict[str, datetime])

    #     assert result == original

    def test_dict_of_str_to_uuid_roundtrip(self, converter):
        """Test dict[str, UUID] serialization and deserialization"""
        original = {
            "id1": UUID("12345678-1234-5678-1234-567812345678"),
            "id2": UUID("87654321-4321-8765-4321-876543218765"),
        }

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, dict[str, UUID])

        assert result == original

    # def test_optional_datetime_with_value_roundtrip(self, converter):
    #     """Test Optional[datetime] with value serialization and deserialization"""
    #     original = datetime(2025, 11, 19, 15, 30, 45)

    #     payload = converter.to_payload(original)
    #     result = converter.from_payload(payload, Optional[datetime])

    #     assert result == original

    def test_optional_datetime_with_none_roundtrip(self, converter):
        """Test Optional[datetime] with None serialization and deserialization"""
        original = None

        payload = converter.to_payload(original)
        result = converter.from_payload(payload, Optional[datetime])

        assert result is None

    # def test_complex_nested_structure(self, converter):
    #     """Test complex nested structure with multiple types"""
    #     original = {
    #         "metadata": {
    #             "created_at": datetime(2025, 11, 19, 15, 30, 45),
    #             "updated_at": datetime(2025, 11, 20, 10, 15, 30),
    #         },
    #         "ids": [
    #             UUID("12345678-1234-5678-1234-567812345678"),
    #             UUID("87654321-4321-8765-4321-876543218765"),
    #         ],
    #         "status": SampleEnum.VALUE_ONE,
    #         "data": base64.b64encode(b"test data").decode('utf-8'),
    #     }

    #     payload = converter.to_payload(original)
    #     result = converter.from_payload(payload, dict)

    #     # Note: Without type hints for nested structures, we get the raw JSON types
    #     assert result["metadata"]["created_at"] == original["metadata"]["created_at"].isoformat()
    #     assert result["metadata"]["updated_at"] == original["metadata"]["updated_at"].isoformat()
    #     assert result["ids"][0] == str(original["ids"][0])
    #     assert result["ids"][1] == str(original["ids"][1])
    #     assert result["status"] == original["status"].value
    #     assert result["data"] == original["data"]


class TestEncoderOnly:
    """Test encoder-specific functionality"""

    # def test_encoder_datetime(self):
    #     """Test datetime encoding to ISO format"""
    #     encoder = KuFlowModelJSONEncoder()
    #     dt = datetime(2025, 11, 19, 15, 30, 45, 123456)

    #     result = json.dumps(dt, cls=KuFlowModelJSONEncoder)

    #     assert result == f'"{dt.isoformat()}"'

    # def test_encoder_date(self):
    #     """Test date encoding to ISO format"""
    #     d = date(2025, 11, 19)

    #     result = json.dumps(d, cls=KuFlowModelJSONEncoder)

    #     assert result == f'"{d.isoformat()}"'

    # def test_encoder_time(self):
    #     """Test time encoding to ISO format"""
    #     t = time(15, 30, 45, 123456)

    #     result = json.dumps(t, cls=KuFlowModelJSONEncoder)

    #     assert result == f'"{t.isoformat()}"'

    # def test_encoder_timedelta(self):
    #     """Test timedelta encoding to seconds"""
    #     td = timedelta(days=1, hours=2, minutes=3, seconds=4)

    #     result = json.dumps(td, cls=KuFlowModelJSONEncoder)

    #     assert result == str(td.total_seconds())

    def test_encoder_uuid(self):
        """Test UUID encoding to string"""
        uuid_obj = UUID("12345678-1234-5678-1234-567812345678")

        result = json.dumps(uuid_obj, cls=KuFlowModelJSONEncoder)

        assert result == f'"{str(uuid_obj)}"'

    # def test_encoder_bytes(self):
    #     """Test bytes encoding to base64"""
    #     data = b"Hello, World!"
    #     expected = base64.b64encode(data).decode('utf-8')

    #     result = json.dumps(data, cls=KuFlowModelJSONEncoder)

    #     assert result == f'"{expected}"'

    # def test_encoder_bytearray(self):
    #     """Test bytearray encoding to base64"""
    #     data = bytearray(b"Hello, World!")
    #     expected = base64.b64encode(data).decode('utf-8')

    #     result = json.dumps(data, cls=KuFlowModelJSONEncoder)

    #     assert result == f'"{expected}"'

    def test_encoder_enum(self):
        """Test Enum encoding to value"""
        enum_val = SampleEnum.VALUE_ONE

        result = json.dumps(enum_val, cls=KuFlowModelJSONEncoder)

        assert result == f'"{enum_val.value}"'

    pass  # Keep class with at least one statement


# class TestConverterOnly:
#     """Test converter-specific functionality"""

#     @pytest.fixture
#     def type_converter(self):
#         return KuFlowModelJSONTypeConverter()

#     # def test_converter_datetime_from_string(self, type_converter):
#     #     """Test datetime deserialization from ISO string"""
#     #     dt_str = "2025-11-19T15:30:45.123456"
#     #     expected = datetime.fromisoformat(dt_str)

#     #     result = type_converter.to_typed_value(datetime, dt_str)

#     #     assert result == expected

#     # def test_converter_date_from_string(self, type_converter):
#     #     """Test date deserialization from ISO string"""
#     #     date_str = "2025-11-19"
#     #     expected = date.fromisoformat(date_str)

#     #     result = type_converter.to_typed_value(date, date_str)

#     #     assert result == expected

#     # def test_converter_time_from_string(self, type_converter):
#     #     """Test time deserialization from ISO string"""
#     #     time_str = "15:30:45.123456"
#     #     expected = time.fromisoformat(time_str)

#     #     result = type_converter.to_typed_value(time, time_str)

#     #     assert result == expected

#     # def test_converter_timedelta_from_seconds(self, type_converter):
#     #     """Test timedelta deserialization from seconds"""
#     #     seconds = 93784.5  # 1 day, 2 hours, 3 minutes, 4.5 seconds
#     #     expected = timedelta(seconds=seconds)

#     #     result = type_converter.to_typed_value(timedelta, seconds)

#     #     assert result == expected

#     # def test_converter_uuid_from_string(self, type_converter):
#     #     """Test UUID deserialization from string"""
#     #     uuid_str = "12345678-1234-5678-1234-567812345678"
#     #     expected = UUID(uuid_str)

#     #     result = type_converter.to_typed_value(UUID, uuid_str)

#     #     assert result == expected

#     # def test_converter_bytes_from_base64(self, type_converter):
#     #     """Test bytes deserialization from base64 string"""
#     #     data = b"Hello, World!"
#     #     base64_str = base64.b64encode(data).decode('utf-8')

#     #     result = type_converter.to_typed_value(bytes, base64_str)

#     #     assert result == data

#     # def test_converter_bytearray_from_base64(self, type_converter):
#     #     """Test bytearray deserialization from base64 string"""
#     #     data = b"Hello, World!"
#     #     base64_str = base64.b64encode(data).decode('utf-8')

#     #     result = type_converter.to_typed_value(bytearray, base64_str)

#     #     assert result == bytearray(data)

#     def test_converter_enum_from_value(self, type_converter):
#         """Test Enum deserialization from value"""
#         enum_value = "value_one"
#         expected = SampleEnum.VALUE_ONE

#         result = value_to_type(SampleEnum, enum_value, [type_converter])

#         # result = type_converter.to_typed_value(SampleEnum, enum_value)

#         assert result == expected

#     pass  # Keep class with at least one statement

#     # def test_converter_none_handling(self, type_converter):
#     #     """Test explicit None handling"""
#     #     result = type_converter.to_typed_value(Optional[str], None)

#     #     assert result is None

#     # def test_converter_list_of_datetime(self, type_converter):
#     #     """Test list[datetime] deserialization"""
#     #     data = ["2025-11-19T15:30:45", "2025-11-20T10:15:30"]
#     #     expected = [datetime.fromisoformat(dt) for dt in data]

#     #     result = type_converter.to_typed_value(list[datetime], data)

#     #     assert result == expected

#     # def test_converter_dict_of_str_to_uuid(self, type_converter):
#     #     """Test dict[str, UUID] deserialization"""
#     #     data = {
#     #         "id1": "12345678-1234-5678-1234-567812345678",
#     #         "id2": "87654321-4321-8765-4321-876543218765",
#     #     }
#     #     expected = {k: UUID(v) for k, v in data.items()}

#     #     result = type_converter.to_typed_value(dict[str, UUID], data)

#     #     assert result == expected

#     # def test_converter_optional_with_value(self, type_converter):
#     #     """Test Optional[datetime] with value"""
#     #     dt_str = "2025-11-19T15:30:45"
#     #     expected = datetime.fromisoformat(dt_str)

#     #     result = type_converter.to_typed_value(Optional[datetime], dt_str)

#     #     assert result == expected

#     # def test_converter_optional_with_none(self, type_converter):
#     #     """Test Optional[datetime] with None"""
#     #     result = type_converter.to_typed_value(Optional[datetime], None)

#     #     assert result is None


# class TestErrorHandling:
#     """Test error handling and validation"""

#     @pytest.fixture
#     def type_converter(self):
#         return KuFlowModelJSONTypeConverter()

#     # def test_invalid_datetime_raises_error(self, type_converter):
#     #     """Test that invalid datetime string raises ValueError"""
#     #     with pytest.raises(ValueError, match="Failed to deserialize datetime"):
#     #         type_converter.to_typed_value(datetime, "invalid-datetime")

#     # def test_invalid_date_raises_error(self, type_converter):
#     #     """Test that invalid date string raises ValueError"""
#     #     with pytest.raises(ValueError, match="Failed to deserialize date"):
#     #         type_converter.to_typed_value(date, "invalid-date")

#     # def test_invalid_time_raises_error(self, type_converter):
#     #     """Test that invalid time string raises ValueError"""
#     #     with pytest.raises(ValueError, match="Failed to deserialize time"):
#     #         type_converter.to_typed_value(time, "invalid-time")

#     # def test_invalid_uuid_raises_error(self, type_converter):
#     #     """Test that invalid UUID string raises ValueError"""
#     #     with pytest.raises(ValueError, match="Failed to deserialize UUID"):
#     #         type_converter.to_typed_value(UUID, "not-a-uuid")

#     # def test_invalid_base64_raises_error(self, type_converter):
#     #     """Test that invalid base64 string raises ValueError"""
#     #     with pytest.raises(ValueError, match="Failed to deserialize bytes"):
#     #         type_converter.to_typed_value(bytes, "not-valid-base64!!!")

#     def test_invalid_enum_value_raises_error(self, type_converter):
#         """Test that invalid enum value raises ValueError"""
#         with pytest.raises(ValueError, match="Failed to deserialize SampleEnum"):
#             type_converter.to_typed_value(SampleEnum, "invalid_value")

#     # def test_invalid_list_item_raises_error(self, type_converter):
#     #     """Test that invalid list item raises ValueError"""
#     #     with pytest.raises(ValueError, match="Failed to deserialize list"):
#     #         type_converter.to_typed_value(list[UUID], ["valid-but-not-uuid"])

#     pass  # Keep class with at least one statement

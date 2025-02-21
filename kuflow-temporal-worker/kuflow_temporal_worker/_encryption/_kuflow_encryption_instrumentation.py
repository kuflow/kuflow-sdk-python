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

from collections.abc import Mapping, Sequence
from typing import Any

import temporalio.api.common.v1
import temporalio.converter


METADATA_KUFLOW_ENCODING_KEY = "x-kuflow-encoding"
METADATA_KUFLOW_ENCODING_ENCRYPTED_NAME = "binary/encrypted?vendor=KuFlow"


class KuFlowEncryptionState:
    encryption_required = False


class KuFlowEncryptionWrapper:
    value: bytes

    def __init__(self, value: bytes) -> None:
        self.value = value


def is_encryption_required(headers: Mapping[str, temporalio.api.common.v1.Payload]) -> bool:
    header_payload = headers.get(METADATA_KUFLOW_ENCODING_KEY)
    if not header_payload:
        return False

    value = temporalio.converter.PayloadConverter.default.from_payload(header_payload)
    if not value:
        return False

    return value == METADATA_KUFLOW_ENCODING_ENCRYPTED_NAME


def add_encryption_encoding(
    headers: Mapping[str, temporalio.api.common.v1.Payload],
) -> Mapping[str, temporalio.api.common.v1.Payload]:
    return {
        **headers,
        METADATA_KUFLOW_ENCODING_KEY: temporalio.converter.PayloadConverter.default.to_payload(
            METADATA_KUFLOW_ENCODING_ENCRYPTED_NAME
        ),
    }


def mark_objects_to_be_encrypted(args: Sequence[Any]) -> Sequence[Any]:
    return [KuFlowEncryptionWrapper(arg) for arg in args]

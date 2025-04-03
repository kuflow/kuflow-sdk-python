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
from typing import Any, Optional

import temporalio.api.common.v1
import temporalio.converter


HEADER_KEY_KUFLOW_ENCODING = "x-kuflow-encoding"
HEADER_KEY_KUFLOW_ENCODING_ENCRYPTED_KEY_ID = "x-kuflow-encoding-encrypted-key-id"
HEADER_VALUE_KUFLOW_ENCODING_ENCRYPTED = "binary/encrypted?vendor=KuFlow"

METADATA_KEY_ENCODING = "encoding"
METADATA_KEY_ENCODING_ENCRYPTED_KEY_ID = "encoding-encrypted-key-id"
METADATA_VALUE_KUFLOW_ENCODING_ENCRYPTED = "binary/encrypted?vendor=KuFlow"


class KuFlowEncryptionState:
    key_id: Optional[str] = None

    def __init__(self, key_id: Optional[str]) -> None:
        self.key_id = key_id

    def merge(self, other: Optional["KuFlowEncryptionState"]):
        if other.key_id is not None:
            self.key_id = other.key_id
        else:
            self.key_id = None


class KuFlowEncryptionWrapper:
    encryption_state: KuFlowEncryptionState

    value: Any

    def __init__(self, encryption_state: KuFlowEncryptionState, value: Any) -> None:
        self.encryption_state = encryption_state
        self.value = value


def retrieve_encryption_state(headers: Mapping[str, temporalio.api.common.v1.Payload]) -> KuFlowEncryptionState:
    if not is_encryption_required(headers):
        return KuFlowEncryptionState(key_id=None)

    key_id_payload = headers.get(HEADER_KEY_KUFLOW_ENCODING_ENCRYPTED_KEY_ID)
    key_id = temporalio.converter.PayloadConverter.default.from_payload(key_id_payload)

    return KuFlowEncryptionState(key_id=key_id)


def is_encryption_required(headers: Mapping[str, temporalio.api.common.v1.Payload]) -> bool:
    header_payload = headers.get(HEADER_KEY_KUFLOW_ENCODING)
    if not header_payload:
        return False

    value = temporalio.converter.PayloadConverter.default.from_payload(header_payload)
    if not value:
        return False

    return value == HEADER_VALUE_KUFLOW_ENCODING_ENCRYPTED


def add_encryption_encoding(
    encryption_state: KuFlowEncryptionState,
    headers: Mapping[str, temporalio.api.common.v1.Payload],
) -> Mapping[str, temporalio.api.common.v1.Payload]:
    if encryption_state.key_id is None:
        return headers

    return {
        **headers,
        HEADER_KEY_KUFLOW_ENCODING: temporalio.converter.PayloadConverter.default.to_payload(
            HEADER_VALUE_KUFLOW_ENCODING_ENCRYPTED
        ),
        HEADER_KEY_KUFLOW_ENCODING_ENCRYPTED_KEY_ID: temporalio.converter.PayloadConverter.default.to_payload(
            encryption_state.key_id
        ),
    }


def mark_objects_to_be_encrypted(encryption_state: KuFlowEncryptionState, args: Sequence[Any]) -> Sequence[Any]:
    if encryption_state.key_id is None:
        return args

    return [KuFlowEncryptionWrapper(encryption_state=encryption_state, value=arg) for arg in args]

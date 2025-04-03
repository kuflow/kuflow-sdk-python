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

from typing import Any, Optional

import temporalio.api.common.v1
from temporalio.converter import EncodingPayloadConverter

from ._kuflow_encryption_instrumentation import (
    METADATA_KEY_ENCODING_ENCRYPTED_KEY_ID,
    KuFlowEncryptionState,
    KuFlowEncryptionWrapper,
)


class KuFlowEncryptionPayloadConverter(EncodingPayloadConverter):
    delegate: EncodingPayloadConverter

    def __init__(self, delegate: EncodingPayloadConverter) -> None:
        self.delegate = delegate

    @property
    def encoding(self) -> str:
        """See base class."""
        return self.delegate.encoding

    def to_payload(self, value: Any) -> Optional[temporalio.api.common.v1.Payload]:
        """See base class."""
        encryption_state: Optional[KuFlowEncryptionState] = None
        if isinstance(value, KuFlowEncryptionWrapper):
            encryption_state = value.encryption_state
            value = value.value

        payload = self.delegate.to_payload(value)

        if payload is not None and encryption_state.key_id is not None:
            payload = temporalio.api.common.v1.Payload(
                metadata={
                    **payload.metadata,
                    METADATA_KEY_ENCODING_ENCRYPTED_KEY_ID: encryption_state.key_id.encode(),
                },
                data=payload.data,
            )

        return payload

    def from_payload(
        self,
        payload: temporalio.api.common.v1.Payload,
        type_hint: Optional[type] = None,
    ) -> Any:
        """See base class."""
        return self.delegate.from_payload(payload, type_hint)

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
from collections.abc import Iterable
from datetime import timedelta

import temporalio.api.common.v1
from temporalio.converter import PayloadCodec

from kuflow_rest import KuFlowRestClient

from ._kuflow_cache import Cache
from ._kuflow_crypto import CIPHERS
from ._kuflow_encryption_instrumentation import (
    METADATA_KEY_ENCODING,
    METADATA_KEY_ENCODING_ENCRYPTED_KEY_ID,
    METADATA_VALUE_KUFLOW_ENCODING_ENCRYPTED,
)


class KuFlowEncryptionPayloadCodec(PayloadCodec):
    rest_client: KuFlowRestClient
    kms_key_cache: Cache[bytes]

    def __init__(self, rest_client: KuFlowRestClient):
        self.rest_client = rest_client
        self.kms_key_cache = Cache[bytes](ttl=timedelta(hours=1))

    async def encode(
        self, payloads: Iterable[temporalio.api.common.v1.Payload]
    ) -> list[temporalio.api.common.v1.Payload]:
        return [await self.encrypt(payload) for payload in payloads]

    async def decode(
        self, payloads: Iterable[temporalio.api.common.v1.Payload]
    ) -> list[temporalio.api.common.v1.Payload]:
        return [await self.decrypt(payload) for payload in payloads]

    async def encrypt(self, payload: temporalio.api.common.v1.Payload) -> temporalio.api.common.v1.Payload:
        if payload.metadata is None or payload.metadata.get(METADATA_KEY_ENCODING_ENCRYPTED_KEY_ID) is None:
            return payload

        key_id = payload.metadata.get(METADATA_KEY_ENCODING_ENCRYPTED_KEY_ID).decode()

        key_value = await self.retrieve_kms_key_cached(id=key_id)

        cipher_text_bytes = CIPHERS.AES_256_GCM.encrypt(key_value, payload.SerializeToString())

        cipher_text_value = base64.b64encode(cipher_text_bytes).decode("utf-8")

        return temporalio.api.common.v1.Payload(
            metadata={
                METADATA_KEY_ENCODING: METADATA_VALUE_KUFLOW_ENCODING_ENCRYPTED.encode(),
                METADATA_KEY_ENCODING_ENCRYPTED_KEY_ID: key_id.encode(),
            },
            data=f"{CIPHERS.AES_256_GCM.algorithm}:{cipher_text_value}".encode(),
        )

    async def decrypt(self, payload: temporalio.api.common.v1.Payload) -> temporalio.api.common.v1.Payload:
        if (
            payload.metadata is None
            or payload.metadata.get(METADATA_KEY_ENCODING, b"").decode() != METADATA_VALUE_KUFLOW_ENCODING_ENCRYPTED
        ):
            return payload

        if payload.data is None:
            raise ValueError("Payload data is missing")

        key_id_bytes = payload.metadata.get(METADATA_KEY_ENCODING_ENCRYPTED_KEY_ID)
        if key_id_bytes is None:
            raise ValueError("Payload key id is missing")

        key_id = key_id_bytes.decode()

        key_value = await self.retrieve_kms_key_cached(id=key_id)

        cipher_text = payload.data.decode()

        cipher_text_algorithm, cipher_text_value = cipher_text.split(":", 1)
        if cipher_text_algorithm is None or cipher_text_value is None:
            raise ValueError("Invalid ciphered data format")

        if cipher_text_algorithm != CIPHERS.AES_256_GCM.algorithm:
            raise ValueError(f"Invalid ciphered data algorithm: {cipher_text_algorithm}")

        cipher_text_value_bytes = base64.b64decode(cipher_text_value)

        plain_text = CIPHERS.AES_256_GCM.decrypt(key_value, cipher_text_value_bytes)

        return temporalio.api.common.v1.Payload.FromString(plain_text)

    async def retrieve_kms_key_cached(self, id: str) -> bytes:
        return await self.kms_key_cache.get(id, lambda: self.retrieve_kms_key(id=id))

    async def retrieve_kms_key(self, id: str) -> bytes:
        key = self.rest_client.kms.retrieve_kms_key(id=id)

        return key.value

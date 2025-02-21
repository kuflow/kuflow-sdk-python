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

from typing import Iterable, List

import temporalio.api.common.v1
from temporalio.converter import PayloadCodec

from kuflow_rest import KuFlowRestClient
from kuflow_rest import models as models_rest

from ._kuflow_encryption_instrumentation import METADATA_KUFLOW_ENCODING_ENCRYPTED_NAME, METADATA_KUFLOW_ENCODING_KEY


class KuFlowEncryptionPayloadCodec(PayloadCodec):
    rest_client: KuFlowRestClient

    def __init__(self, rest_client: KuFlowRestClient):
        self.rest_client = rest_client

    async def encode(
        self, payloads: Iterable[temporalio.api.common.v1.Payload]
    ) -> List[temporalio.api.common.v1.Payload]:
        payloads_to_encrypt = list(filter(need_payload_be_encrypted, payloads))

        payloads_encrypted = await self.encrypt(payloads_to_encrypt)

        return [
            payloads_encrypted[i] if need_payload_be_encrypted(payload) else payload
            for i, payload in enumerate(payloads)
        ]

    async def decode(
        self, payloads: Iterable[temporalio.api.common.v1.Payload]
    ) -> List[temporalio.api.common.v1.Payload]:
        payloads_to_decrypt = list(filter(is_payload_encrypted, payloads))

        payloads_decrypted = await self.decrypt(payloads_to_decrypt)

        return [
            payloads_decrypted[i] if is_payload_encrypted(payload) else payload for i, payload in enumerate(payloads)
        ]

    async def encrypt(self, payloads: List[temporalio.api.common.v1.Payload]) -> List[temporalio.api.common.v1.Payload]:
        if not payloads:
            return payloads

        request_payloads = list(map(transform_payload_to_vault_codec_payload, payloads))

        response = self.rest_client.vault.codec_encode(
            vault_codec_encode_params=models_rest.VaultCodecPayloads(payloads=request_payloads)
        )

        return list(map(transform_vault_codec_payload_to_payload, response.payloads))

    async def decrypt(self, payloads: List[temporalio.api.common.v1.Payload]) -> List[temporalio.api.common.v1.Payload]:
        if not payloads:
            return payloads

        request_payloads = list(map(transform_payload_to_vault_codec_payload, payloads))

        response = self.rest_client.vault.codec_decode(
            vault_codec_decode_params=models_rest.VaultCodecPayloads(payloads=request_payloads)
        )

        return list(map(transform_vault_codec_payload_to_payload, response.payloads))


def need_payload_be_encrypted(payload: temporalio.api.common.v1.Payload) -> bool:
    return (
        payload.metadata is not None
        and payload.metadata.get(METADATA_KUFLOW_ENCODING_KEY, b"").decode() == METADATA_KUFLOW_ENCODING_ENCRYPTED_NAME
    )


def is_payload_encrypted(payload: temporalio.api.common.v1.Payload) -> bool:
    return (
        payload.metadata is not None
        and payload.metadata.get("encoding", b"").decode() == METADATA_KUFLOW_ENCODING_ENCRYPTED_NAME
    )


def transform_payload_to_vault_codec_payload(
    payload: temporalio.api.common.v1.Payload,
) -> models_rest.VaultCodecPayload:
    return models_rest.VaultCodecPayload(
        metadata=payload.metadata,
        data=payload.data,
    )


def transform_vault_codec_payload_to_payload(
    payload: models_rest.VaultCodecPayload,
) -> temporalio.api.common.v1.Payload:
    return temporalio.api.common.v1.Payload(
        metadata={k: bytes(v) for k, v in payload.metadata.items()},
        data=bytes(payload.data),
    )

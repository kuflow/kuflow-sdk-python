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

from typing import Any

from .. import models as _models
from .._generated import KuFlowRestClient as KuFlowRestClientGenerated


class VaultOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`authentication` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def codec_encode(
        self,
        vault_codec_encode_params: _models.VaultCodecPayloads,
        **kwargs: Any,
    ) -> _models.VaultCodecPayloads:
        """Encode the requested payloads.

        Encode the requested payloads.

        :param vault_codec_encode_params: Payloads to encode. Required.
        :type vault_codec_encode_params: ~kuflow.rest.models.VaultCodecPayloads
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: VaultCodecPayloads
        :rtype: ~kuflow.rest.models.VaultCodecPayloads
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.vault.codec_encode(vault_codec_encode_params=vault_codec_encode_params, **kwargs)

    def codec_decode(
        self,
        vault_codec_decode_params: _models.VaultCodecPayloads,
        **kwargs: Any,
    ) -> _models.VaultCodecPayloads:
        """Decode the requested payloads.

        Decode the requested payloads.

        :param vault_codec_decode_params: Payloads to decode. Required.
        :type vault_codec_decode_params: ~kuflow.rest.models.VaultCodecPayloads
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: VaultCodecPayloads
        :rtype: ~kuflow.rest.models.VaultCodecPayloads
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.vault.codec_decode(vault_codec_decode_params=vault_codec_decode_params, **kwargs)

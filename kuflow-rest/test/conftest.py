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

import pytest
from azure.core.pipeline.policies import SansIOHTTPPolicy

from kuflow_rest._generated import KuFlowRestClient as KuFlowRestClientGenerated
from kuflow_rest._kuflow_rest_client import ClientSecretCredential

from ._stubs import ENDPOINT, StubClientFactory, StubTransport


@pytest.fixture
def stub_client() -> StubClientFactory:
    """Builds a generated client whose transport is a ``StubTransport`` answering with the given response."""

    def factory(
        status_code: int, content: bytes = b"", content_type: str = "application/json"
    ) -> tuple[KuFlowRestClientGenerated, StubTransport]:
        transport = StubTransport(status_code=status_code, content=content, content_type=content_type)
        kuflow_client = KuFlowRestClientGenerated(
            credential=ClientSecretCredential(client_id="client-id", client_secret="client-secret"),
            endpoint=ENDPOINT,
            authentication_policy=SansIOHTTPPolicy(),
            transport=transport,
        )

        return kuflow_client, transport

    return factory

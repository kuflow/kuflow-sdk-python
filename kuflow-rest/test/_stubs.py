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

from typing import Callable

from azure.core.pipeline.transport import HttpTransport
from azure.core.rest._http_response_impl import HttpResponseImpl

from kuflow_rest._generated import KuFlowRestClient as KuFlowRestClientGenerated


ENDPOINT = "https://api.kuflow.test/v2024-06-14"


class StubInternalResponse:
    """Stands for the raw response of a real HTTP library; the pipeline only closes it."""

    def close(self) -> None:
        pass


class StubTransport(HttpTransport):
    """Answers every request with the same status and body, recording the requests sent."""

    def __init__(self, status_code: int, content: bytes = b"", content_type: str = "application/json") -> None:
        self.status_code = status_code
        self.content = content
        self.content_type = content_type
        self.requests: list = []

    def __enter__(self) -> "StubTransport":
        return self

    def __exit__(self, *args) -> None:
        pass

    def open(self) -> None:
        pass

    def close(self) -> None:
        pass

    def send(self, request, **kwargs):
        self.requests.append(request)

        response = HttpResponseImpl(
            request=request,
            internal_response=StubInternalResponse(),
            status_code=self.status_code,
            reason="",
            content_type=self.content_type,
            headers={"Content-Type": self.content_type},
            stream_download_generator=None,
        )
        response._content = self.content

        return response


StubClientFactory = Callable[..., tuple[KuFlowRestClientGenerated, StubTransport]]

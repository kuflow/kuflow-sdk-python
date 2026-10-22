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

import pytest
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline.transport import HttpRequest
from azure.core.rest._http_response_impl import HttpResponseImpl
from temporalio.api.failure.v1 import Failure
from temporalio.converter import DataConverter
from temporalio.exceptions import ApplicationError

from kuflow_rest import models as models_rest
from kuflow_temporal_common import KuFlowFailureType, create_application_error


DEFAULT_ERROR = {
    "timestamp": "2026-10-22T10:00:00.000Z",
    "status": 0,
    "message": "error",
    "errors": [{"code": "process.notFound", "message": "Process not found", "location": "id", "locationType": "PATH"}],
}

# The error map every generated operation of kuflow_rest uses.
ERROR_MAP = {
    401: ClientAuthenticationError,
    404: ResourceNotFoundError,
    409: ResourceExistsError,
    304: ResourceNotModifiedError,
}


class StubInternalResponse:
    def close(self) -> None:
        pass


def raise_rest_error(status_code: int, content: bytes) -> HttpResponseError:
    """Raise the error the generated operations raise for a non 2xx answer (see ``_process_operations.py``)."""
    request = HttpRequest("GET", "https://api.kuflow.test/v2024-06-14/processes/id")
    response = HttpResponseImpl(
        request=request,
        internal_response=StubInternalResponse(),
        status_code=status_code,
        reason="",
        content_type="application/json",
        headers={"Content-Type": "application/json"},
        stream_download_generator=None,
    )
    response._content = content

    with pytest.raises(HttpResponseError) as error:
        map_error(status_code=status_code, response=response, error_map=ERROR_MAP)
        try:
            model = models_rest.DefaultError.deserialize(json.loads(content))
        except Exception:
            model = None
        raise HttpResponseError(response=response, model=model)

    return error.value


def default_error_body(status_code: int) -> bytes:
    return json.dumps({**DEFAULT_ERROR, "status": status_code}).encode()


def test_given_a_mapped_rest_error_when_create_application_error_then_attaches_the_default_error_from_the_body():
    rest_error = raise_rest_error(404, default_error_body(404))
    assert isinstance(rest_error, ResourceNotFoundError)
    assert rest_error.model is None

    error = create_application_error(rest_error)

    assert error.type == KuFlowFailureType.ACTIVITIES_REST_FAILURE
    assert error.__cause__ is rest_error
    assert error.details == ({**DEFAULT_ERROR, "status": 404},)


def test_given_an_unmapped_rest_error_when_create_application_error_then_attaches_the_deserialized_default_error():
    rest_error = raise_rest_error(500, default_error_body(500))
    assert rest_error.model is not None

    error = create_application_error(rest_error)

    assert error.type == KuFlowFailureType.ACTIVITIES_REST_FAILURE
    assert error.details == ({**DEFAULT_ERROR, "status": 500},)


def test_given_a_rest_error_without_body_when_create_application_error_then_has_no_details():
    rest_error = raise_rest_error(304, b"")
    assert isinstance(rest_error, ResourceNotModifiedError)

    error = create_application_error(rest_error)

    assert error.type == KuFlowFailureType.ACTIVITIES_REST_FAILURE
    assert error.details == ()


def test_given_a_rest_error_with_a_non_json_body_when_create_application_error_then_has_no_details():
    error = create_application_error(raise_rest_error(502, b"<html>Bad gateway</html>"))

    assert error.type == KuFlowFailureType.ACTIVITIES_REST_FAILURE
    assert error.details == ()


def test_given_a_non_rest_error_when_create_application_error_then_wraps_it_as_cause_without_details():
    cause = ValueError("boom")

    error = create_application_error(cause)

    assert error.type == KuFlowFailureType.ACTIVITIES_FAILURE
    assert error.__cause__ is cause
    assert error.details == ()


def test_given_an_application_error_when_create_application_error_then_returns_it_untouched():
    original = ApplicationError("validation", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE)

    assert create_application_error(original) is original


def test_given_a_rest_error_when_temporal_encodes_the_failure_then_keeps_type_and_default_error():
    error = create_application_error(raise_rest_error(404, default_error_body(404)))
    failure = Failure()

    DataConverter.default.failure_converter.to_failure(error, DataConverter.default.payload_converter, failure)

    assert failure.application_failure_info.type == KuFlowFailureType.ACTIVITIES_REST_FAILURE
    details = DataConverter.default.payload_converter.from_payloads(failure.application_failure_info.details.payloads)
    assert details == [{**DEFAULT_ERROR, "status": 404}]
    assert failure.cause.message

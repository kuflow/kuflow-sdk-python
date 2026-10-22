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
from urllib.parse import parse_qs, urlparse

import pytest
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

from kuflow_rest import models
from kuflow_rest.operations import ProcessOperations

from ._stubs import ENDPOINT, StubClientFactory, StubTransport


PROCESS_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f6"
PROCESS_ACTION_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f7"
DEFAULT_ERROR_BODY = b'{"timestamp": "2026-10-22T10:00:00Z", "status": %d, "message": "error", "errors": []}'
PROCESS_ACTION_BODY = json.dumps(
    {
        "id": PROCESS_ACTION_ID,
        "type": "CREATE_TASK",
        "status": "COMPLETED",
        "processActionDefinitionRef": {"id": "0192b7a1-0000-7000-8000-000000000002", "code": "ACTION"},
    }
).encode()


def create_process_operations(
    stub_client: StubClientFactory, status_code: int, content: bytes = b""
) -> tuple[ProcessOperations, StubTransport]:
    kuflow_client, transport = stub_client(status_code=status_code, content=content)

    return ProcessOperations(kuflow_client), transport


def test_given_a_process_when_delete_process_then_sends_delete_request_and_returns_none(stub_client):
    process_operations, transport = create_process_operations(stub_client, status_code=204)

    result = process_operations.delete_process(PROCESS_ID)

    assert result is None
    assert len(transport.requests) == 1
    assert transport.requests[0].method == "DELETE"
    assert transport.requests[0].url == f"{ENDPOINT}/processes/{PROCESS_ID}"


def test_given_a_process_with_work_in_progress_when_delete_process_then_raises_resource_exists_error(stub_client):
    process_operations, _ = create_process_operations(stub_client, status_code=409, content=DEFAULT_ERROR_BODY % 409)

    with pytest.raises(ResourceExistsError) as error:
        process_operations.delete_process(PROCESS_ID)

    assert error.value.status_code == 409


def test_given_an_unknown_process_when_delete_process_then_raises_resource_not_found_error(stub_client):
    process_operations, _ = create_process_operations(stub_client, status_code=404, content=DEFAULT_ERROR_BODY % 404)

    with pytest.raises(ResourceNotFoundError):
        process_operations.delete_process(PROCESS_ID)


def test_given_a_deleted_process_payload_when_deserialize_then_exposes_deleted_fields():
    process = models.Process.deserialize(
        {
            "objectType": "PROCESS",
            "id": PROCESS_ID,
            "state": "COMPLETED",
            "processDefinitionRef": {"id": "d", "version": "v", "code": "C"},
            "tenantId": "t",
            "deletedBy": "0192b7a1-0000-7000-8000-000000000001",
            "deletedAt": "2026-10-22T10:00:00Z",
        }
    )

    assert isinstance(process, models.AbstractDeleted)
    assert isinstance(process, models.AbstractAudited)
    assert process.deleted_by == "0192b7a1-0000-7000-8000-000000000001"
    assert process.deleted_at is not None


def test_given_state_and_initiator_filters_when_find_processes_then_sends_them_as_query_params(stub_client):
    process_operations, transport = create_process_operations(
        stub_client, status_code=200, content=b'{"objectType": "PROCESS_PAGE", "content": [], "metadata": {}}'
    )

    process_operations.find_processes(
        state=models.ProcessState.RUNNING,
        initiator_id="0192b7a1-0000-7000-8000-000000000001",
        initiator_email=["a@kuflow.com", "b@kuflow.com"],
    )

    query = parse_qs(urlparse(transport.requests[0].url).query)
    assert transport.requests[0].method == "GET"
    assert query["state"] == ["RUNNING"]
    assert query["initiatorId"] == ["0192b7a1-0000-7000-8000-000000000001"]
    assert query["initiatorEmail"] == ["a@kuflow.com", "b@kuflow.com"]


def test_given_a_process_when_create_process_action_then_posts_the_params_and_returns_the_action(stub_client):
    process_operations, transport = create_process_operations(stub_client, status_code=200, content=PROCESS_ACTION_BODY)
    params = models.ProcessActionCreateParams(id=PROCESS_ACTION_ID, process_action_definition_code="ACTION")

    process_action = process_operations.create_process_action(PROCESS_ID, process_action_create_params=params)

    assert transport.requests[0].method == "POST"
    assert transport.requests[0].url == f"{ENDPOINT}/processes/{PROCESS_ID}/actions"
    assert json.loads(transport.requests[0].content) == {
        "id": PROCESS_ACTION_ID,
        "processActionDefinitionCode": "ACTION",
    }
    assert isinstance(process_action, models.ProcessAction)
    assert process_action.id == PROCESS_ACTION_ID


def test_given_a_process_action_when_retrieve_process_action_then_gets_it_by_id(stub_client):
    process_operations, transport = create_process_operations(stub_client, status_code=200, content=PROCESS_ACTION_BODY)

    process_action = process_operations.retrieve_process_action(PROCESS_ID, action_id=PROCESS_ACTION_ID)

    assert transport.requests[0].method == "GET"
    assert transport.requests[0].url == f"{ENDPOINT}/processes/{PROCESS_ID}/actions/{PROCESS_ACTION_ID}"
    assert process_action.id == PROCESS_ACTION_ID


def test_given_a_process_action_when_cancel_process_action_then_posts_the_cancel_action(stub_client):
    process_operations, transport = create_process_operations(stub_client, status_code=200, content=PROCESS_ACTION_BODY)

    process_action = process_operations.cancel_process_action(PROCESS_ID, action_id=PROCESS_ACTION_ID)

    assert transport.requests[0].method == "POST"
    assert transport.requests[0].url == f"{ENDPOINT}/processes/{PROCESS_ID}/actions/{PROCESS_ACTION_ID}/~actions/cancel"
    assert process_action.id == PROCESS_ACTION_ID

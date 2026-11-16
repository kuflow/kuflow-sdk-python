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

import asyncio
import json
from unittest.mock import MagicMock

import pytest
from temporalio.api.common.v1 import Payload
from temporalio.exceptions import ApplicationError

from kuflow_rest import models as models_rest
from kuflow_temporal_activity_kuflow import KuFlowActivities
from kuflow_temporal_activity_kuflow import models as models_temporal
from kuflow_temporal_activity_kuflow.converter import KuFlowComposableEncodingPayloadConverter
from kuflow_temporal_common import KuFlowFailureType


PROCESS_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f6"
PROCESS_ACTION_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f7"
BUSINESS_ARTIFACT_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f8"
PROCESS_ACTION_JSON = {
    "id": PROCESS_ACTION_ID,
    "type": "SEND_WORKFLOW_SIGNAL",
    "status": "COMPLETED",
    "processActionDefinitionRef": {"id": "0192b7a1-0000-7000-8000-000000000002", "code": "SIGNAL"},
}


@pytest.fixture
def kuflow_client() -> MagicMock:
    return MagicMock()


@pytest.fixture
def kuflow_activities(kuflow_client: MagicMock) -> KuFlowActivities:
    return KuFlowActivities(kuflow_client)


@pytest.fixture
def converter() -> KuFlowComposableEncodingPayloadConverter:
    return KuFlowComposableEncodingPayloadConverter()


def activity_name(activity_method) -> str:
    return activity_method.__temporal_activity_definition.name


def to_json(converter: KuFlowComposableEncodingPayloadConverter, value) -> dict:
    payload = converter.to_payload(value)
    assert payload is not None

    return json.loads(payload.data)


def from_json(converter: KuFlowComposableEncodingPayloadConverter, value: dict, type_hint: type):
    payload = Payload(metadata={"encoding": b"json/plain"}, data=json.dumps(value).encode())

    return converter.from_payload(payload, type_hint)


def assert_validation_error(error: pytest.ExceptionInfo, field: str) -> None:
    assert isinstance(error.value, ApplicationError)
    assert error.value.type == KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
    assert error.value.non_retryable
    assert f"'{field}'" in str(error.value)


def test_given_the_activities_when_registered_then_every_new_activity_uses_the_java_name(kuflow_activities):
    names = {activity_name(it) for it in kuflow_activities.activities}

    assert {
        "KuFlow_Engine_deleteProcess",
        "KuFlow_Engine_createProcessAction",
        "KuFlow_Engine_retrieveProcessAction",
        "KuFlow_Engine_cancelProcessAction",
        "KuFlow_Engine_prepareBusinessArtifactActionStartProcess",
    } <= names
    assert len(names) == len(kuflow_activities.activities)


def test_given_a_process_when_delete_process_then_deletes_it_and_returns_an_empty_response(
    kuflow_activities, kuflow_client, converter
):
    request = from_json(converter, {"processId": PROCESS_ID}, models_temporal.ProcessDeleteRequest)

    response = asyncio.run(kuflow_activities.delete_process(request))

    kuflow_client.process.delete_process.assert_called_once_with(id=PROCESS_ID)
    assert isinstance(response, models_temporal.ProcessDeleteResponse)
    assert to_json(converter, response) == {}


def test_given_no_process_id_when_delete_process_then_raises_a_validation_error(kuflow_activities, kuflow_client):
    with pytest.raises(ApplicationError) as error:
        asyncio.run(kuflow_activities.delete_process(models_temporal.ProcessDeleteRequest(process_id="")))

    assert_validation_error(error, "process_id")
    kuflow_client.process.delete_process.assert_not_called()


def test_given_a_process_action_request_when_create_process_action_then_invokes_it_with_the_params(
    kuflow_activities, kuflow_client, converter
):
    process_action = models_rest.ProcessAction.deserialize(PROCESS_ACTION_JSON)
    kuflow_client.process.create_process_action.return_value = process_action
    request = from_json(
        converter,
        {
            "processId": PROCESS_ID,
            "id": PROCESS_ACTION_ID,
            "processActionDefinitionCode": "SIGNAL",
            "sendWorkflowSignal": {"input": {"FIELD": "value"}},
        },
        models_temporal.ProcessActionCreateRequest,
    )

    response = asyncio.run(kuflow_activities.create_process_action(request))

    call = kuflow_client.process.create_process_action.call_args
    params = call.kwargs["process_action_create_params"]
    assert call.kwargs["id"] == PROCESS_ID
    assert params.id == PROCESS_ACTION_ID
    assert params.process_action_definition_code == "SIGNAL"
    assert params.send_workflow_signal.input == {"FIELD": "value"}
    assert response.process_action is process_action
    assert to_json(converter, response) == {"processAction": PROCESS_ACTION_JSON}


def test_given_no_action_definition_code_when_create_process_action_then_raises_a_validation_error(kuflow_activities):
    request = models_temporal.ProcessActionCreateRequest(process_id=PROCESS_ID, process_action_definition_code="")

    with pytest.raises(ApplicationError) as error:
        asyncio.run(kuflow_activities.create_process_action(request))

    assert_validation_error(error, "process_action_definition_code")


def test_given_a_process_action_when_retrieve_process_action_then_returns_it(
    kuflow_activities, kuflow_client, converter
):
    process_action = models_rest.ProcessAction.deserialize(PROCESS_ACTION_JSON)
    kuflow_client.process.retrieve_process_action.return_value = process_action
    request = from_json(
        converter,
        {"processId": PROCESS_ID, "processActionId": PROCESS_ACTION_ID},
        models_temporal.ProcessActionRetrieveRequest,
    )

    response = asyncio.run(kuflow_activities.retrieve_process_action(request))

    kuflow_client.process.retrieve_process_action.assert_called_once_with(id=PROCESS_ID, action_id=PROCESS_ACTION_ID)
    assert response.process_action is process_action


def test_given_a_process_action_when_cancel_process_action_then_cancels_it(kuflow_activities, kuflow_client):
    process_action = models_rest.ProcessAction.deserialize(PROCESS_ACTION_JSON)
    kuflow_client.process.cancel_process_action.return_value = process_action
    request = models_temporal.ProcessActionCancelRequest(process_id=PROCESS_ID, process_action_id=PROCESS_ACTION_ID)

    response = asyncio.run(kuflow_activities.cancel_process_action(request))

    kuflow_client.process.cancel_process_action.assert_called_once_with(id=PROCESS_ID, action_id=PROCESS_ACTION_ID)
    assert response.process_action is process_action


def test_given_no_process_action_id_when_cancel_process_action_then_raises_a_validation_error(kuflow_activities):
    request = models_temporal.ProcessActionCancelRequest(process_id=PROCESS_ID, process_action_id="")

    with pytest.raises(ApplicationError) as error:
        asyncio.run(kuflow_activities.cancel_process_action(request))

    assert_validation_error(error, "process_action_id")


def test_given_a_start_process_action_when_prepare_then_returns_the_prepared_metadata(
    kuflow_activities, kuflow_client, converter
):
    prepare = models_rest.BusinessArtifactActionStartProcessPrepare.deserialize({"metadata": {"value": {"F": "v"}}})
    kuflow_client.business_artifact.prepare_business_artifact_action_start_process.return_value = prepare
    request = from_json(
        converter,
        {"businessArtifactId": BUSINESS_ARTIFACT_ID, "businessArtifactActionDefinitionCode": "START"},
        models_temporal.BusinessArtifactActionStartProcessPrepareRequest,
    )

    response = asyncio.run(kuflow_activities.prepare_business_artifact_action_start_process(request))

    call = kuflow_client.business_artifact.prepare_business_artifact_action_start_process.call_args
    assert call.kwargs["id"] == BUSINESS_ARTIFACT_ID
    assert call.kwargs[
        "business_artifact_action_start_process_prepare_params"
    ].business_artifact_action_definition_code == ("START")
    assert response.business_artifact_action_start_process_prepare is prepare
    assert to_json(converter, response) == {
        "businessArtifactActionStartProcessPrepare": {"metadata": {"value": {"F": "v"}}}
    }


def test_given_no_business_artifact_id_when_prepare_start_process_then_raises_a_validation_error(kuflow_activities):
    request = models_temporal.BusinessArtifactActionStartProcessPrepareRequest(
        business_artifact_id="", business_artifact_action_definition_code="START"
    )

    with pytest.raises(ApplicationError) as error:
        asyncio.run(kuflow_activities.prepare_business_artifact_action_start_process(request))

    assert_validation_error(error, "business_artifact_id")


def test_given_state_and_initiator_filters_when_find_processes_then_forwards_them(
    kuflow_activities, kuflow_client, converter
):
    request = from_json(
        converter,
        {
            "states": ["RUNNING"],
            "initiatorIds": ["0192b7a1-0000-7000-8000-000000000001"],
            "initiatorEmails": ["a@kuflow.com"],
        },
        models_temporal.ProcessFindRequest,
    )

    asyncio.run(kuflow_activities.find_processes(request))

    call = kuflow_client.process.find_processes.call_args
    assert call.kwargs["state"] == [models_rest.ProcessState.RUNNING]
    assert call.kwargs["initiator_id"] == ["0192b7a1-0000-7000-8000-000000000001"]
    assert call.kwargs["initiator_email"] == ["a@kuflow.com"]


def test_given_a_thread_id_when_create_process_item_then_forwards_it(kuflow_activities, kuflow_client, converter):
    thread_id = "0192b7a1-0000-7000-8000-000000000009"
    request = from_json(
        converter,
        {
            "id": "0192b7a1-0000-7000-8000-000000000008",
            "type": "MESSAGE",
            "processId": PROCESS_ID,
            "processItemThreadId": thread_id,
            "message": {"text": "hello"},
        },
        models_temporal.ProcessItemCreateRequest,
    )

    asyncio.run(kuflow_activities.create_process_item(request))

    params = kuflow_client.process_item.create_process_item.call_args.kwargs["process_item_create_params"]
    assert params.process_item_thread_id == thread_id


def test_given_a_thread_item_with_a_thread_id_when_create_process_item_then_raises_a_validation_error(
    kuflow_activities,
):
    request = models_temporal.ProcessItemCreateRequest(
        id="0192b7a1-0000-7000-8000-000000000008",
        type=models_rest.ProcessItemType.THREAD,
        process_id=PROCESS_ID,
        process_item_definition_code="THREAD",
        process_item_thread_id="0192b7a1-0000-7000-8000-000000000009",
    )

    with pytest.raises(ApplicationError) as error:
        asyncio.run(kuflow_activities.create_process_item(request))

    assert_validation_error(error, "process_item_thread_id")


FEED_ITEM_ID = "0192b7a1-0000-7000-8000-000000000010"
FEED_ITEM_THREAD_ID = "0192b7a1-0000-7000-8000-000000000011"
BUSINESS_ARTIFACT_DEFINITION_ID = "0192b7a1-0000-7000-8000-000000000012"


def business_artifact_feed_item_create_request(
    item_type: models_rest.BusinessArtifactFeedItemType, **kwargs
) -> models_temporal.BusinessArtifactFeedItemCreateRequest:
    return models_temporal.BusinessArtifactFeedItemCreateRequest(
        id=FEED_ITEM_ID, type=item_type, business_artifact_definition_id=BUSINESS_ARTIFACT_DEFINITION_ID, **kwargs
    )


def test_given_a_thread_when_create_business_artifact_feed_item_then_sends_the_thread_and_returns_the_item(
    kuflow_activities, kuflow_client
):
    business_artifact_feed_item = MagicMock()
    kuflow_client.business_artifact.create_business_artifact_feed_item.return_value = business_artifact_feed_item
    thread = models_rest.BusinessArtifactFeedItemThreadParams(
        title="Invoice import", description="Importing the invoices"
    )
    request = business_artifact_feed_item_create_request(models_rest.BusinessArtifactFeedItemType.THREAD, thread=thread)

    response = asyncio.run(kuflow_activities.create_business_artifact_feed_item(request))

    call = kuflow_client.business_artifact.create_business_artifact_feed_item.call_args
    params = call.kwargs["business_artifact_feed_item_create_params"]
    assert params.type == models_rest.BusinessArtifactFeedItemType.THREAD
    assert params.thread is thread
    assert params.message is None
    assert response.business_artifact_feed_item is business_artifact_feed_item


@pytest.mark.parametrize(
    ("item_type", "kwargs", "field"),
    [
        (models_rest.BusinessArtifactFeedItemType.THREAD, {}, "thread.title"),
        (
            models_rest.BusinessArtifactFeedItemType.THREAD,
            {"thread": models_rest.BusinessArtifactFeedItemThreadParams(title=None, description="A description")},
            "thread.title",
        ),
        (
            models_rest.BusinessArtifactFeedItemType.THREAD,
            {
                "thread": models_rest.BusinessArtifactFeedItemThreadParams(title="A thread"),
                "business_artifact_feed_item_thread_id": FEED_ITEM_THREAD_ID,
            },
            "business_artifact_feed_item_thread_id",
        ),
        (models_rest.BusinessArtifactFeedItemType.MESSAGE, {}, "message.text"),
        (
            models_rest.BusinessArtifactFeedItemType.MESSAGE,
            {
                "message": models_rest.BusinessArtifactFeedItemMessageParams(
                    text=None, level=models_rest.BusinessArtifactFeedItemMessageLevel.INFO
                )
            },
            "message.text",
        ),
    ],
    ids=[
        "thread-without-thread",
        "thread-without-title",
        "thread-inside-a-thread",
        "message-without-message",
        "message-without-text",
    ],
)
def test_given_an_item_not_matching_its_type_when_create_business_artifact_feed_item_then_raises_a_validation_error(
    kuflow_activities, kuflow_client, item_type, kwargs, field
):
    request = business_artifact_feed_item_create_request(item_type, **kwargs)

    with pytest.raises(ApplicationError) as error:
        asyncio.run(kuflow_activities.create_business_artifact_feed_item(request))

    assert_validation_error(error, field)
    kuflow_client.business_artifact.create_business_artifact_feed_item.assert_not_called()


def test_given_a_java_type_when_create_business_artifact_feed_item_then_the_type_checks_apply(
    kuflow_activities, kuflow_client, converter
):
    request = from_json(
        converter,
        {
            "id": FEED_ITEM_ID,
            "type": "THREAD",
            "businessArtifactDefinitionId": BUSINESS_ARTIFACT_DEFINITION_ID,
            "businessArtifactFeedItemThreadId": FEED_ITEM_THREAD_ID,
            "thread": {"title": "A thread"},
        },
        models_temporal.BusinessArtifactFeedItemCreateRequest,
    )

    with pytest.raises(ApplicationError) as error:
        asyncio.run(kuflow_activities.create_business_artifact_feed_item(request))

    assert_validation_error(error, "business_artifact_feed_item_thread_id")
    kuflow_client.business_artifact.create_business_artifact_feed_item.assert_not_called()


def test_given_a_metadata_patch_request_when_serialize_then_uses_the_java_json_patch_key(converter):
    request = models_temporal.ProcessMetadataPatchRequest(
        process_id=PROCESS_ID, json_patch=[models_rest.JsonPatchOperation(op="add", path="/FIELD", value="v")]
    )

    assert to_json(converter, request) == {
        "processId": PROCESS_ID,
        "jsonPatch": [{"op": "add", "path": "/FIELD", "value": "v"}],
    }


def test_given_a_tenant_user_response_when_deserialize_then_keeps_the_tenant_user(converter):
    response = from_json(
        converter,
        {"tenantUser": {"objectType": "TENANT_USER", "id": "u1", "tenantId": "t1", "metadata": {"value": {}}}},
        models_temporal.TenantUserRetrieveResponse,
    )

    assert isinstance(response.tenant_user, models_rest.TenantUser)
    assert response.tenant_user.tenant_id == "t1"


def test_given_a_java_request_with_payloads_when_deserialize_then_ignores_them(converter):
    request = from_json(
        converter,
        {"processId": PROCESS_ID, "payloads": {"key": "value"}},
        models_temporal.ProcessDeleteRequest,
    )

    assert request.process_id == PROCESS_ID
    assert to_json(converter, request) == {"processId": PROCESS_ID}

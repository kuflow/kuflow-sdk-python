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

"""Every KuFlow activity: the Java-shaped request is mapped to the right REST call, and its required fields are checked.

The requests are built from the JSON a workflow in any language sends (Java keys), so these tests also pin the
contract shared with the Java and JS SDKs.
"""

import asyncio
import json
from dataclasses import dataclass, field
from typing import Any, Optional
from unittest.mock import MagicMock

import pytest
from temporalio.api.common.v1 import Payload
from temporalio.exceptions import ApplicationError

from kuflow_rest import Model
from kuflow_rest import models as models_rest
from kuflow_temporal_activity_kuflow import KuFlowActivities
from kuflow_temporal_activity_kuflow.converter import KuFlowComposableEncodingPayloadConverter
from kuflow_temporal_common import KuFlowFailureType


ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f6"
OTHER_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f7"
TENANT_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f8"
JSON_VALUE = {"value": {"FIELD": "v"}}
JSON_PATCH = [{"op": "add", "path": "/FIELD", "value": "v"}]

PROCESS = models_rest.Process.deserialize({"id": ID, "state": "RUNNING", "tenantId": TENANT_ID})
PROCESS_PAGE = models_rest.ProcessPage.deserialize({"content": [], "metadata": {"size": 25, "page": 0}})
PROCESS_ITEM = models_rest.ProcessItem.deserialize({"id": ID, "type": "TASK", "processId": ID})
PROCESS_ITEM_PAGE = models_rest.ProcessItemPage.deserialize({"content": [], "metadata": {"size": 25, "page": 0}})
PROCESS_ACTION = models_rest.ProcessAction.deserialize({"id": OTHER_ID, "type": "CREATE_TASK", "status": "COMPLETED"})
AI_ASSISTANCE = models_rest.ProcessItemAiAssistance.deserialize({"processItemId": ID})
PRINCIPAL = models_rest.Principal.deserialize({"id": ID, "type": "USER", "name": "John"})
TENANT_USER = models_rest.TenantUser.deserialize({"id": ID, "tenantId": TENANT_ID})
BUSINESS_ARTIFACT = models_rest.BusinessArtifact.deserialize({"id": ID, "data": JSON_VALUE})
BUSINESS_ARTIFACT_PAGE = models_rest.BusinessArtifactPage.deserialize({"content": [], "metadata": {"size": 25}})
BUSINESS_ARTIFACT_ACTION = models_rest.BusinessArtifactAction.deserialize(
    {"id": OTHER_ID, "type": "START_WORKFLOW", "status": "REQUESTED"}
)
CREATE_ARTIFACT_PREPARE = models_rest.BusinessArtifactActionCreateArtifactPrepare.deserialize({"data": JSON_VALUE})
START_PROCESS_PREPARE = models_rest.BusinessArtifactActionStartProcessPrepare.deserialize({"metadata": JSON_VALUE})


def json_value() -> models_rest.JsonValue:
    return models_rest.JsonValue(value={"FIELD": "v"})


def json_patch() -> list[models_rest.JsonPatchOperation]:
    return [models_rest.JsonPatchOperation(op="add", path="/FIELD", value="v")]


@dataclass
class Case:
    activity: str
    name: str
    request: dict[str, Any]
    client_method: str
    kwargs: dict[str, Any]
    returns: Optional[Model] = None
    response_key: Optional[str] = None
    required: list[tuple[tuple[str, ...], str]] = field(default_factory=list)


def required(*names: str) -> list[tuple[tuple[str, ...], str]]:
    return [((name,), f"'{name}' is required") for name in names]


CASES = [
    Case(
        "retrieve_principal",
        "retrievePrincipal",
        {"principalId": ID},
        "principal.retrieve_principal",
        {"id": ID},
        PRINCIPAL,
        "principal",
        required("principal_id"),
    ),
    Case(
        "retrieve_tenant_user",
        "retrieveTenantUser",
        {"tenantUserId": ID},
        "tenant_user.retrieve_tenant_user",
        {"id": ID},
        TENANT_USER,
        "tenantUser",
        required("tenant_user_id"),
    ),
    Case(
        "find_processes",
        "findProcesses",
        {
            "page": 1,
            "size": 10,
            "sorts": ["createdAt,desc"],
            "tenantIds": [TENANT_ID],
            "processDefinitionIds": [ID],
            "processDefinitionCodes": ["PD"],
            "states": ["RUNNING"],
            "initiatorIds": [OTHER_ID],
            "initiatorEmails": ["a@kuflow.com"],
            "metadata": ["FIELD eq 1"],
            "deleted": "INCLUDE",
        },
        "process.find_processes",
        {
            "size": 10,
            "page": 1,
            "sort": ["createdAt,desc"],
            "tenant_id": [TENANT_ID],
            "process_definition_id": [ID],
            "process_definition_code": ["PD"],
            "state": ["RUNNING"],
            "initiator_id": [OTHER_ID],
            "initiator_email": ["a@kuflow.com"],
            "metadata": ["FIELD eq 1"],
            "deleted": "INCLUDE",
        },
        PROCESS_PAGE,
        "processes",
    ),
    Case(
        "retrieve_process",
        "retrieveProcess",
        {"processId": ID},
        "process.retrieve_process",
        {"id": ID},
        PROCESS,
        "process",
        required("process_id"),
    ),
    Case(
        "delete_process",
        "deleteProcess",
        {"processId": ID},
        "process.delete_process",
        {"id": ID},
        required=required("process_id"),
    ),
    Case(
        "update_process_entity",
        "updateProcessEntity",
        {"processId": ID, "entity": JSON_VALUE},
        "process.update_process_entity",
        {"id": ID, "process_entity_update_params": models_rest.ProcessEntityUpdateParams(entity=json_value())},
        PROCESS,
        "process",
        required("process_id", "entity"),
    ),
    Case(
        "patch_process_entity",
        "patchProcessEntity",
        {"processId": ID, "jsonPatch": JSON_PATCH},
        "process.patch_process_entity",
        {"id": ID, "json_patch": json_patch()},
        PROCESS,
        "process",
        required("process_id", "json_patch"),
    ),
    Case(
        "update_process_metadata",
        "updateProcessMetadata",
        {"processId": ID, "metadata": JSON_VALUE},
        "process.update_process_metadata",
        {"id": ID, "process_metadata_update_params": models_rest.ProcessMetadataUpdateParams(metadata=json_value())},
        PROCESS,
        "process",
        required("process_id", "metadata"),
    ),
    Case(
        "patch_process_metadata",
        "patchProcessMetadata",
        {"processId": ID, "jsonPatch": JSON_PATCH},
        "process.patch_process_metadata",
        {"id": ID, "json_patch": json_patch()},
        PROCESS,
        "process",
        required("process_id", "json_patch"),
    ),
    Case(
        "change_process_initiator",
        "changeProcessInitiator",
        {"processId": ID, "initiatorEmail": "a@kuflow.com"},
        "process.change_process_initiator",
        {
            "id": ID,
            "process_change_initiator_params": models_rest.ProcessChangeInitiatorParams(initiator_email="a@kuflow.com"),
        },
        PROCESS,
        "process",
        required("process_id") + [(("initiator_id", "initiator_email"), "'initiator_id' or 'initiator_email'")],
    ),
    Case(
        "create_process_action",
        "createProcessAction",
        {
            "processId": ID,
            "id": OTHER_ID,
            "processActionDefinitionCode": "ACTION",
            "createTask": {"processItemThreadId": OTHER_ID},
        },
        "process.create_process_action",
        {
            "id": ID,
            "process_action_create_params": models_rest.ProcessActionCreateParams(
                id=OTHER_ID,
                process_action_definition_code="ACTION",
                create_task=models_rest.ProcessActionCreateParamsCreateTask(process_item_thread_id=OTHER_ID),
            ),
        },
        PROCESS_ACTION,
        "processAction",
        required("process_id", "process_action_definition_code"),
    ),
    Case(
        "retrieve_process_action",
        "retrieveProcessAction",
        {"processId": ID, "processActionId": OTHER_ID},
        "process.retrieve_process_action",
        {"id": ID, "action_id": OTHER_ID},
        PROCESS_ACTION,
        "processAction",
        required("process_id", "process_action_id"),
    ),
    Case(
        "cancel_process_action",
        "cancelProcessAction",
        {"processId": ID, "processActionId": OTHER_ID},
        "process.cancel_process_action",
        {"id": ID, "action_id": OTHER_ID},
        PROCESS_ACTION,
        "processAction",
        required("process_id", "process_action_id"),
    ),
    Case(
        "cancel_process_items",
        "cancelProcessItems",
        {"processId": ID, "processItemIds": [OTHER_ID]},
        "process.cancel_process_items",
        {"id": ID, "process_item_id": [OTHER_ID]},
        PROCESS,
        "process",
        required("process_id"),
    ),
    Case(
        "find_process_items",
        "findProcessItems",
        {
            "page": 1,
            "size": 10,
            "sorts": ["createdAt"],
            "tenantIds": [TENANT_ID],
            "processIds": [ID],
            "types": ["TASK"],
            "taskStates": ["READY"],
            "processItemDefinitionCodes": ["TASK"],
            "processDefinitionIds": [OTHER_ID],
            "processDefinitionCodes": ["PD"],
            "deleted": "ONLY",
        },
        "process_item.find_process_items",
        {
            "size": 10,
            "page": 1,
            "sort": ["createdAt"],
            "process_id": [ID],
            "type": ["TASK"],
            "task_state": ["READY"],
            "process_item_definition_code": ["TASK"],
            "process_definition_id": [OTHER_ID],
            "process_definition_code": ["PD"],
            "tenant_id": [TENANT_ID],
            "deleted": "ONLY",
        },
        PROCESS_ITEM_PAGE,
        "processItems",
    ),
    Case(
        "retrieve_process_item",
        "retrieveProcessItem",
        {"processItemId": ID},
        "process_item.retrieve_process_item",
        {"id": ID},
        PROCESS_ITEM,
        "processItem",
        required("process_item_id"),
    ),
    Case(
        "create_process_item",
        "createProcessItem",
        {
            "id": OTHER_ID,
            "type": "TASK",
            "processId": ID,
            "ownerEmail": "a@kuflow.com",
            "processItemDefinitionCode": "TASK",
            "task": {"data": JSON_VALUE},
        },
        "process_item.create_process_item",
        {
            "process_item_create_params": models_rest.ProcessItemCreateParams(
                id=OTHER_ID,
                type=models_rest.ProcessItemType.TASK,
                process_id=ID,
                owner_email="a@kuflow.com",
                process_item_definition_code="TASK",
                task=models_rest.ProcessItemTaskCreateParams(data=json_value()),
            )
        },
        PROCESS_ITEM,
        "processItem",
        required("id", "process_id", "type", "process_item_definition_code"),
    ),
    Case(
        "complete_process_item_task",
        "completeProcessItemTask",
        {"processItemId": ID},
        "process_item.complete_process_item_task",
        {"id": ID},
        PROCESS_ITEM,
        "processItem",
        required("process_item_id"),
    ),
    Case(
        "claim_process_item_task",
        "claimProcessItemTask",
        {"processItemId": ID},
        "process_item.claim_process_item_task",
        {"id": ID},
        PROCESS_ITEM,
        "processItem",
        required("process_item_id"),
    ),
    Case(
        "assign_process_item_task",
        "assignProcessItemTask",
        {"processItemId": ID, "ownerId": OTHER_ID},
        "process_item.assign_process_item_task",
        {"id": ID, "process_item_task_assign_params": models_rest.ProcessItemTaskAssignParams(owner_id=OTHER_ID)},
        PROCESS_ITEM,
        "processItem",
        required("process_item_id") + [(("owner_id", "owner_email"), "'owner_id' or 'owner_email'")],
    ),
    Case(
        "update_process_item_task_data",
        "updateProcessItemTaskData",
        {"processItemId": ID, "data": JSON_VALUE},
        "process_item.update_process_item_task_data",
        {
            "id": ID,
            "process_item_task_data_update_params": models_rest.ProcessItemTaskDataUpdateParams(data=json_value()),
        },
        PROCESS_ITEM,
        "processItem",
        required("process_item_id", "data"),
    ),
    Case(
        "patch_process_item_task_data",
        "patchProcessItemTaskData",
        {"processItemId": ID, "jsonPatch": JSON_PATCH},
        "process_item.patch_process_item_task_data",
        {"id": ID, "json_patch": json_patch()},
        PROCESS_ITEM,
        "processItem",
        required("process_item_id", "json_patch"),
    ),
    Case(
        "update_process_item_task_context_data",
        "updateProcessItemTaskContextData",
        {"processItemId": ID, "data": JSON_VALUE},
        "process_item.update_process_item_task_context_data",
        {
            "id": ID,
            "process_item_task_context_data_update_params": models_rest.ProcessItemTaskContextDataUpdateParams(
                data=json_value()
            ),
        },
        PROCESS_ITEM,
        "processItem",
        required("process_item_id", "data"),
    ),
    Case(
        "append_process_item_task_log",
        "appendProcessItemTaskLog",
        {"processItemId": ID, "message": "hello", "level": "INFO"},
        "process_item.append_process_item_task_log",
        {
            "id": ID,
            "process_item_task_append_log_params": models_rest.ProcessItemTaskAppendLogParams(
                message="hello", level=models_rest.ProcessItemTaskLogLevel.INFO
            ),
        },
        PROCESS_ITEM,
        "processItem",
        required("process_item_id", "level", "message"),
    ),
    Case(
        "retrieve_process_item_ai_assistance",
        "retrieveProcessItemAiAssistance",
        {"processItemId": ID},
        "process_item.retrieve_process_item_ai_assistance",
        {"id": ID},
        AI_ASSISTANCE,
        "processItemAiAssistance",
        required("process_item_id"),
    ),
    Case(
        "generate_process_item_ai_assistance",
        "generateProcessItemAiAssistance",
        {"processItemId": ID, "requestId": OTHER_ID},
        "process_item.generate_process_item_ai_assistance",
        {
            "id": ID,
            "process_item_ai_assistance_generate_params": models_rest.ProcessItemAiAssistanceGenerateParams(
                request_id=OTHER_ID
            ),
        },
        AI_ASSISTANCE,
        "processItemAiAssistance",
        required("process_item_id", "request_id"),
    ),
    Case(
        "find_business_artifacts",
        "findBusinessArtifacts",
        {
            "page": 1,
            "size": 10,
            "sorts": ["createdAt"],
            "tenantIds": [TENANT_ID],
            "businessArtifactDefinitionIds": [ID],
            "businessArtifactDefinitionCodes": ["BAD"],
            "values": ["FIELD eq 1"],
            "deleted": "EXCLUDE",
        },
        "business_artifact.find_business_artifacts",
        {
            "size": 10,
            "page": 1,
            "sort": ["createdAt"],
            "tenant_id": [TENANT_ID],
            "business_artifact_definition_id": [ID],
            "business_artifact_definition_code": ["BAD"],
            "value": ["FIELD eq 1"],
            "deleted": "EXCLUDE",
        },
        BUSINESS_ARTIFACT_PAGE,
        "businessArtifacts",
    ),
    Case(
        "create_business_artifact",
        "createBusinessArtifact",
        {"id": OTHER_ID, "businessArtifactDefinitionCode": "BAD", "tenantId": TENANT_ID, "data": JSON_VALUE},
        "business_artifact.create_business_artifact",
        {
            "business_artifact_create_params": models_rest.BusinessArtifactCreateParams(
                id=OTHER_ID, business_artifact_definition_code="BAD", tenant_id=TENANT_ID, data=json_value()
            )
        },
        BUSINESS_ARTIFACT,
        "businessArtifact",
        [
            (
                ("business_artifact_definition_id", "business_artifact_definition_code"),
                "'business_artifact_definition_id' or 'business_artifact_definition_code'",
            )
        ],
    ),
    Case(
        "retrieve_business_artifact",
        "retrieveBusinessArtifact",
        {"businessArtifactId": ID},
        "business_artifact.retrieve_business_artifact",
        {"id": ID},
        BUSINESS_ARTIFACT,
        "businessArtifact",
        required("business_artifact_id"),
    ),
    Case(
        "delete_business_artifact",
        "deleteBusinessArtifact",
        {"businessArtifactId": ID},
        "business_artifact.delete_business_artifact",
        {"id": ID},
        required=required("business_artifact_id"),
    ),
    Case(
        "update_business_artifact",
        "updateBusinessArtifact",
        {"businessArtifactId": ID, "data": JSON_VALUE},
        "business_artifact.update_business_artifact_data",
        {
            "id": ID,
            "business_artifact_data_update_params": models_rest.BusinessArtifactDataUpdateParams(data=json_value()),
        },
        BUSINESS_ARTIFACT,
        "businessArtifact",
        required("business_artifact_id", "data"),
    ),
    Case(
        "patch_business_artifact",
        "patchBusinessArtifact",
        {"businessArtifactId": ID, "jsonPatch": JSON_PATCH},
        "business_artifact.patch_business_artifact_data",
        {"id": ID, "json_patch": json_patch()},
        BUSINESS_ARTIFACT,
        "businessArtifact",
        required("business_artifact_id", "json_patch"),
    ),
    Case(
        "create_business_artifact_action",
        "createBusinessArtifactAction",
        {
            "businessArtifactId": ID,
            "id": OTHER_ID,
            "businessArtifactActionDefinitionCode": "ACTION",
            "startWorkflow": {"input": {"FIELD": "v"}},
        },
        "business_artifact.create_business_artifact_action",
        {
            "id": ID,
            "business_artifact_action_create_params": models_rest.BusinessArtifactActionCreateParams(
                id=OTHER_ID,
                business_artifact_action_definition_code="ACTION",
                start_workflow=models_rest.BusinessArtifactActionCreateParamsStartWorkflow.deserialize(
                    {"input": {"FIELD": "v"}}
                ),
            ),
        },
        BUSINESS_ARTIFACT_ACTION,
        "businessArtifactAction",
        required("business_artifact_id", "business_artifact_action_definition_code"),
    ),
    Case(
        "retrieve_business_artifact_action",
        "retrieveBusinessArtifactAction",
        {"businessArtifactId": ID, "businessArtifactActionId": OTHER_ID},
        "business_artifact.retrieve_business_artifact_action",
        {"id": ID, "action_id": OTHER_ID},
        BUSINESS_ARTIFACT_ACTION,
        "businessArtifactAction",
        required("business_artifact_id", "business_artifact_action_id"),
    ),
    Case(
        "cancel_business_artifact_action",
        "cancelBusinessArtifactAction",
        {"businessArtifactId": ID, "businessArtifactActionId": OTHER_ID},
        "business_artifact.cancel_business_artifact_action",
        {"id": ID, "action_id": OTHER_ID},
        BUSINESS_ARTIFACT_ACTION,
        "businessArtifactAction",
        required("business_artifact_id", "business_artifact_action_id"),
    ),
    Case(
        "prepare_business_artifact_action_create_artifact",
        "prepareBusinessArtifactActionCreateArtifact",
        {"businessArtifactId": ID, "businessArtifactActionDefinitionCode": "ACTION"},
        "business_artifact.prepare_business_artifact_action_create_artifact",
        {
            "id": ID,
            "business_artifact_action_create_artifact_prepare_params": (
                models_rest.BusinessArtifactActionCreateArtifactPrepareParams(
                    business_artifact_action_definition_code="ACTION"
                )
            ),
        },
        CREATE_ARTIFACT_PREPARE,
        "businessArtifactActionCreateArtifactPrepare",
        required("business_artifact_id", "business_artifact_action_definition_code"),
    ),
    Case(
        "prepare_business_artifact_action_start_process",
        "prepareBusinessArtifactActionStartProcess",
        {"businessArtifactId": ID, "businessArtifactActionDefinitionCode": "ACTION"},
        "business_artifact.prepare_business_artifact_action_start_process",
        {
            "id": ID,
            "business_artifact_action_start_process_prepare_params": (
                models_rest.BusinessArtifactActionStartProcessPrepareParams(
                    business_artifact_action_definition_code="ACTION"
                )
            ),
        },
        START_PROCESS_PREPARE,
        "businessArtifactActionStartProcessPrepare",
        required("business_artifact_id", "business_artifact_action_definition_code"),
    ),
]

VALIDATION_CASES = [(case, fields, fragment) for case in CASES for fields, fragment in case.required]


@pytest.fixture
def converter() -> KuFlowComposableEncodingPayloadConverter:
    return KuFlowComposableEncodingPayloadConverter()


def activity_method(activities: KuFlowActivities, case: Case):
    return getattr(activities, case.activity)


def request_of(converter: KuFlowComposableEncodingPayloadConverter, case: Case) -> Model:
    request_type = getattr(KuFlowActivities, case.activity).__annotations__["request"]
    payload = Payload(metadata={"encoding": b"json/plain"}, data=json.dumps(case.request).encode())

    return converter.from_payload(payload, request_type)


def client_method(kuflow_client: MagicMock, case: Case) -> MagicMock:
    target = kuflow_client
    for name in case.client_method.split("."):
        target = getattr(target, name)

    return target


def comparable(value: Any) -> Any:
    if isinstance(value, Model):
        return value.serialize(keep_readonly=True)
    if isinstance(value, list):
        return [comparable(it) for it in value]
    if isinstance(value, dict):
        return {k: comparable(v) for k, v in value.items()}

    return value


def test_given_the_cases_when_listed_then_every_activity_has_one():
    activities = KuFlowActivities(MagicMock())

    names = {it.__temporal_activity_definition.name for it in activities.activities}

    assert names == {f"KuFlow_Engine_{case.name}" for case in CASES}
    assert len(activities.activities) == len(CASES)


@pytest.mark.parametrize("case", CASES, ids=[it.name for it in CASES])
def test_given_a_java_shaped_request_when_the_activity_runs_then_calls_the_rest_operation(converter, case: Case):
    kuflow_client = MagicMock()
    client_method(kuflow_client, case).return_value = case.returns
    activities = KuFlowActivities(kuflow_client)
    method = activity_method(activities, case)

    response = asyncio.run(method(request_of(converter, case)))

    assert method.__temporal_activity_definition.name == f"KuFlow_Engine_{case.name}"
    call = client_method(kuflow_client, case)
    call.assert_called_once()
    assert call.call_args.args == ()
    assert comparable(call.call_args.kwargs) == comparable(case.kwargs)
    response_payload = converter.to_payload(response)
    assert response_payload is not None
    expected_response = {} if case.response_key is None else {case.response_key: comparable(case.returns)}
    assert json.loads(response_payload.data) == expected_response


@pytest.mark.parametrize(
    ("case", "fields", "fragment"),
    VALIDATION_CASES,
    ids=[f"{case.name}-{'-'.join(fields)}" for case, fields, _ in VALIDATION_CASES],
)
def test_given_a_request_without_a_required_field_when_the_activity_runs_then_fails_without_calling_rest(
    converter, case: Case, fields: tuple[str, ...], fragment: str
):
    kuflow_client = MagicMock()
    activities = KuFlowActivities(kuflow_client)
    request = request_of(converter, case)
    for name in fields:
        setattr(request, name, None)

    with pytest.raises(ApplicationError) as error:
        asyncio.run(activity_method(activities, case)(request))

    assert error.value.type == KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
    assert error.value.non_retryable
    assert fragment in str(error.value)
    client_method(kuflow_client, case).assert_not_called()

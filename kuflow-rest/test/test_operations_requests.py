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

"""Every hand-written operation must reach the generated client with the right request.

Each case calls one wrapper of ``kuflow_rest.operations`` against a ``StubTransport`` and checks the HTTP method, the
path, the query parameters and the JSON body sent, plus that the answer is deserialized into the declared model.
"""

import io
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from urllib.parse import parse_qs, urlparse

import pytest

from kuflow_rest import models
from kuflow_rest import operations as ops

from ._stubs import ENDPOINT


ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f6"
ACTION_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f7"
TENANT_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f8"
DOCUMENT_URI = f"ku:process/{ID}/document/0192b7a1-0000-7000-8000-000000000003"
BASE_PATH = urlparse(ENDPOINT).path

PROCESS = {"objectType": "PROCESS", "id": ID, "state": "RUNNING", "tenantId": TENANT_ID}
PROCESS_ITEM = {"objectType": "PROCESS_ITEM", "id": ID, "type": "TASK", "processId": ID, "tenantId": TENANT_ID}
BUSINESS_ARTIFACT = {"objectType": "BUSINESS_ARTIFACT", "id": ID}
BUSINESS_ARTIFACT_ACTION = {"id": ACTION_ID, "type": "START_WORKFLOW", "status": "REQUESTED"}
PAGE = {"content": [], "metadata": {"size": 25, "page": 0, "totalElements": 0, "totalPages": 0}}
JSON_VALUE = models.JsonValue(value={"FIELD": "v"})
JSON_VALUE_BODY = {"value": {"FIELD": "v"}}
JSON_PATCH = [models.JsonPatchOperation(op="add", path="/FIELD", value="value")]
JSON_PATCH_BODY = [{"op": "add", "path": "/FIELD", "value": "value"}]


def document() -> models.Document:
    return models.Document(file_name="hello.txt", content_type="text/plain", file_content=io.BytesIO(b"hello"))


@dataclass
class Case:
    id: str
    operations: Callable[[Any], Any]
    call: Callable[[Any], Any]
    method: str
    path: str
    query: Optional[dict[str, list[str]]] = None
    body: Any = None
    status: int = 200
    response: Any = field(default_factory=dict)
    response_content_type: str = "application/json"
    result: Optional[type] = None


CASES = [
    # Authentication
    Case(
        "create_authentication",
        ops.AuthenticationOperations,
        lambda o: o.create_authentication(models.AuthenticationCreateParams(type="ENGINE_TOKEN", tenant_id=TENANT_ID)),
        "POST",
        "/authentications",
        body={"type": "ENGINE_TOKEN", "tenantId": TENANT_ID},
        response={"id": ID, "type": "ENGINE_TOKEN"},
        result=models.Authentication,
    ),
    # Business Artifact
    Case(
        "find_business_artifacts",
        ops.BusinessArtifactOperations,
        lambda o: o.find_business_artifacts(
            sort="createdAt,desc",
            tenant_id=TENANT_ID,
            business_artifact_definition_id=ID,
            business_artifact_definition_code="CODE",
            value="FIELD eq 1",
            deleted=models.DeletedQueryParam.INCLUDE,
        ),
        "GET",
        "/business-artifacts",
        query={
            "size": ["25"],
            "page": ["0"],
            "sort": ["createdAt,desc"],
            "tenantId": [TENANT_ID],
            "businessArtifactDefinitionId": [ID],
            "businessArtifactDefinitionCode": ["CODE"],
            "value": ["FIELD eq 1"],
            "deleted": ["INCLUDE"],
        },
        response=PAGE,
        result=models.BusinessArtifactPage,
    ),
    Case(
        "create_business_artifact",
        ops.BusinessArtifactOperations,
        lambda o: o.create_business_artifact(
            models.BusinessArtifactCreateParams(id=ID, business_artifact_definition_id=ID, data=JSON_VALUE)
        ),
        "POST",
        "/business-artifacts",
        body={"id": ID, "businessArtifactDefinitionId": ID, "data": JSON_VALUE_BODY},
        response=BUSINESS_ARTIFACT,
        result=models.BusinessArtifact,
    ),
    Case(
        "retrieve_business_artifact",
        ops.BusinessArtifactOperations,
        lambda o: o.retrieve_business_artifact(ID),
        "GET",
        f"/business-artifacts/{ID}",
        response=BUSINESS_ARTIFACT,
        result=models.BusinessArtifact,
    ),
    Case(
        "delete_business_artifact",
        ops.BusinessArtifactOperations,
        lambda o: o.delete_business_artifact(ID),
        "DELETE",
        f"/business-artifacts/{ID}",
        status=204,
        response=None,
    ),
    Case(
        "update_business_artifact_data",
        ops.BusinessArtifactOperations,
        lambda o: o.update_business_artifact_data(ID, models.BusinessArtifactDataUpdateParams(data=JSON_VALUE)),
        "PUT",
        f"/business-artifacts/{ID}/data",
        body={"data": JSON_VALUE_BODY},
        response=BUSINESS_ARTIFACT,
        result=models.BusinessArtifact,
    ),
    Case(
        "patch_business_artifact_data",
        ops.BusinessArtifactOperations,
        lambda o: o.patch_business_artifact_data(ID, JSON_PATCH),
        "PATCH",
        f"/business-artifacts/{ID}/data",
        body=JSON_PATCH_BODY,
        response=BUSINESS_ARTIFACT,
        result=models.BusinessArtifact,
    ),
    Case(
        "create_business_artifact_action",
        ops.BusinessArtifactOperations,
        lambda o: o.create_business_artifact_action(
            ID, models.BusinessArtifactActionCreateParams(id=ACTION_ID, business_artifact_action_definition_code="A")
        ),
        "POST",
        f"/business-artifacts/{ID}/actions",
        body={"id": ACTION_ID, "businessArtifactActionDefinitionCode": "A"},
        response=BUSINESS_ARTIFACT_ACTION,
        result=models.BusinessArtifactAction,
    ),
    Case(
        "retrieve_business_artifact_action",
        ops.BusinessArtifactOperations,
        lambda o: o.retrieve_business_artifact_action(ID, ACTION_ID),
        "GET",
        f"/business-artifacts/{ID}/actions/{ACTION_ID}",
        response=BUSINESS_ARTIFACT_ACTION,
        result=models.BusinessArtifactAction,
    ),
    Case(
        "cancel_business_artifact_action",
        ops.BusinessArtifactOperations,
        lambda o: o.cancel_business_artifact_action(ID, ACTION_ID),
        "POST",
        f"/business-artifacts/{ID}/actions/{ACTION_ID}/~actions/cancel",
        response=BUSINESS_ARTIFACT_ACTION,
        result=models.BusinessArtifactAction,
    ),
    Case(
        "prepare_business_artifact_action_create_artifact",
        ops.BusinessArtifactOperations,
        lambda o: o.prepare_business_artifact_action_create_artifact(
            ID, models.BusinessArtifactActionCreateArtifactPrepareParams(business_artifact_action_definition_code="A")
        ),
        "POST",
        f"/business-artifacts/{ID}/~actions/prepare-create-artifact",
        body={"businessArtifactActionDefinitionCode": "A"},
        response={"data": JSON_VALUE_BODY},
        result=models.BusinessArtifactActionCreateArtifactPrepare,
    ),
    Case(
        "upload_business_artifact_document",
        ops.BusinessArtifactOperations,
        lambda o: o.upload_business_artifact_document(ID, document()),
        "POST",
        f"/business-artifacts/{ID}/~actions/upload-document",
        query={"fileContentType": ["text/plain"], "fileName": ["hello.txt"]},
        response={"documentUri": DOCUMENT_URI},
        result=models.DocumentReference,
    ),
    Case(
        "download_business_artifact_document",
        ops.BusinessArtifactOperations,
        lambda o: b"".join(o.download_business_artifact_document(ID, document_uri=DOCUMENT_URI)),
        "GET",
        f"/business-artifacts/{ID}/~actions/download-document",
        query={"documentUri": [DOCUMENT_URI]},
        response=b"hello",
        response_content_type="application/octet-stream",
        result=bytes,
    ),
    # Principal
    Case(
        "find_principals",
        ops.PrincipalOperations,
        lambda o: o.find_principals(
            sort="name", type=models.PrincipalType.USER, group_id=ID, group_code="G", tenant_id=TENANT_ID
        ),
        "GET",
        "/principals",
        query={
            "size": ["25"],
            "page": ["0"],
            "sort": ["name"],
            "type": ["USER"],
            "groupId": [ID],
            "groupCode": ["G"],
            "tenantId": [TENANT_ID],
        },
        response=PAGE,
        result=models.PrincipalPage,
    ),
    Case(
        "retrieve_principal",
        ops.PrincipalOperations,
        lambda o: o.retrieve_principal(ID),
        "GET",
        f"/principals/{ID}",
        response={"id": ID, "type": "USER", "name": "John"},
        result=models.Principal,
    ),
    # Process
    Case(
        "create_process",
        ops.ProcessOperations,
        lambda o: o.create_process(models.ProcessCreateParams(id=ID, process_definition_id=ID)),
        "POST",
        "/processes",
        body={"id": ID, "processDefinitionId": ID},
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "retrieve_process",
        ops.ProcessOperations,
        lambda o: o.retrieve_process(ID),
        "GET",
        f"/processes/{ID}",
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "complete_process",
        ops.ProcessOperations,
        lambda o: o.complete_process(ID),
        "POST",
        f"/processes/{ID}/~actions/complete",
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "cancel_process",
        ops.ProcessOperations,
        lambda o: o.cancel_process(ID),
        "POST",
        f"/processes/{ID}/~actions/cancel",
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "cancel_process_items",
        ops.ProcessOperations,
        lambda o: o.cancel_process_items(ID, process_item_id=ACTION_ID),
        "POST",
        f"/processes/{ID}/~actions/cancel-process-items",
        query={"processItemId": [ACTION_ID]},
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "change_process_initiator",
        ops.ProcessOperations,
        lambda o: o.change_process_initiator(ID, models.ProcessChangeInitiatorParams(initiator_email="a@kuflow.com")),
        "POST",
        f"/processes/{ID}/~actions/change-initiator",
        body={"initiatorEmail": "a@kuflow.com"},
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "update_process_metadata",
        ops.ProcessOperations,
        lambda o: o.update_process_metadata(ID, models.ProcessMetadataUpdateParams(metadata=JSON_VALUE)),
        "PUT",
        f"/processes/{ID}/metadata",
        body={"metadata": JSON_VALUE_BODY},
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "patch_process_metadata",
        ops.ProcessOperations,
        lambda o: o.patch_process_metadata(ID, JSON_PATCH),
        "PATCH",
        f"/processes/{ID}/metadata",
        body=JSON_PATCH_BODY,
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "update_process_entity",
        ops.ProcessOperations,
        lambda o: o.update_process_entity(ID, models.ProcessEntityUpdateParams(entity=JSON_VALUE)),
        "PUT",
        f"/processes/{ID}/entity",
        body={"entity": JSON_VALUE_BODY},
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "patch_process_entity",
        ops.ProcessOperations,
        lambda o: o.patch_process_entity(ID, JSON_PATCH),
        "PATCH",
        f"/processes/{ID}/entity",
        body=JSON_PATCH_BODY,
        response=PROCESS,
        result=models.Process,
    ),
    Case(
        "upload_process_document",
        ops.ProcessOperations,
        lambda o: o.upload_process_document(ID, document()),
        "POST",
        f"/processes/{ID}/~actions/upload-document",
        query={"fileContentType": ["text/plain"], "fileName": ["hello.txt"]},
        response={"documentUri": DOCUMENT_URI},
        result=models.DocumentReference,
    ),
    Case(
        "download_process_document",
        ops.ProcessOperations,
        lambda o: b"".join(o.download_process_document(ID, document_uri=DOCUMENT_URI)),
        "GET",
        f"/processes/{ID}/~actions/download-document",
        query={"documentUri": [DOCUMENT_URI]},
        response=b"hello",
        response_content_type="application/octet-stream",
        result=bytes,
    ),
    # Process Item
    Case(
        "find_process_items",
        ops.ProcessItemOperations,
        lambda o: o.find_process_items(
            sort="createdAt",
            process_id=ID,
            type=[models.ProcessItemType.TASK],
            task_state=models.ProcessItemTaskState.READY,
            process_item_definition_code="TASK",
            process_definition_id=ID,
            process_definition_code="PD",
            tenant_id=TENANT_ID,
            deleted=models.DeletedQueryParam.ONLY,
        ),
        "GET",
        "/process-items",
        query={
            "size": ["25"],
            "page": ["0"],
            "sort": ["createdAt"],
            "processId": [ID],
            "type": ["TASK"],
            "taskState": ["READY"],
            "processItemDefinitionCode": ["TASK"],
            "processDefinitionId": [ID],
            "processDefinitionCode": ["PD"],
            "tenantId": [TENANT_ID],
            "deleted": ["ONLY"],
        },
        response=PAGE,
        result=models.ProcessItemPage,
    ),
    Case(
        "create_process_item",
        ops.ProcessItemOperations,
        lambda o: o.create_process_item(
            models.ProcessItemCreateParams(
                id=ID, type=models.ProcessItemType.TASK, process_id=ID, process_item_definition_code="TASK"
            )
        ),
        "POST",
        "/process-items",
        body={"id": ID, "type": "TASK", "processId": ID, "processItemDefinitionCode": "TASK"},
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "retrieve_process_item",
        ops.ProcessItemOperations,
        lambda o: o.retrieve_process_item(ID),
        "GET",
        f"/process-items/{ID}",
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "claim_process_item_task",
        ops.ProcessItemOperations,
        lambda o: o.claim_process_item_task(ID),
        "POST",
        f"/process-items/{ID}/task/~actions/claim",
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "assign_process_item_task",
        ops.ProcessItemOperations,
        lambda o: o.assign_process_item_task(ID, models.ProcessItemTaskAssignParams(owner_email="a@kuflow.com")),
        "POST",
        f"/process-items/{ID}/task/~actions/assign",
        body={"ownerEmail": "a@kuflow.com"},
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "complete_process_item_task",
        ops.ProcessItemOperations,
        lambda o: o.complete_process_item_task(ID),
        "POST",
        f"/process-items/{ID}/task/~actions/complete",
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "append_process_item_task_log",
        ops.ProcessItemOperations,
        lambda o: o.append_process_item_task_log(
            ID, models.ProcessItemTaskAppendLogParams(message="hello", level=models.ProcessItemTaskLogLevel.INFO)
        ),
        "POST",
        f"/process-items/{ID}/task/~actions/append-log",
        body={"message": "hello", "level": "INFO"},
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "update_process_item_task_data",
        ops.ProcessItemOperations,
        lambda o: o.update_process_item_task_data(ID, models.ProcessItemTaskDataUpdateParams(data=JSON_VALUE)),
        "PUT",
        f"/process-items/{ID}/task/data",
        body={"data": JSON_VALUE_BODY},
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "patch_process_item_task_data",
        ops.ProcessItemOperations,
        lambda o: o.patch_process_item_task_data(ID, JSON_PATCH),
        "PATCH",
        f"/process-items/{ID}/task/data",
        body=JSON_PATCH_BODY,
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "update_process_item_task_context_data",
        ops.ProcessItemOperations,
        lambda o: o.update_process_item_task_context_data(
            ID, models.ProcessItemTaskContextDataUpdateParams(data=JSON_VALUE)
        ),
        "PUT",
        f"/process-items/{ID}/task/context-data",
        body={"data": JSON_VALUE_BODY},
        response=PROCESS_ITEM,
        result=models.ProcessItem,
    ),
    Case(
        "retrieve_process_item_ai_assistance",
        ops.ProcessItemOperations,
        lambda o: o.retrieve_process_item_ai_assistance(ID),
        "GET",
        f"/process-items/{ID}/~actions/ai-assistance",
        response={"processItemId": ID},
        result=models.ProcessItemAiAssistance,
    ),
    Case(
        "generate_process_item_ai_assistance",
        ops.ProcessItemOperations,
        lambda o: o.generate_process_item_ai_assistance(
            ID, models.ProcessItemAiAssistanceGenerateParams(request_id=ACTION_ID)
        ),
        "POST",
        f"/process-items/{ID}/~actions/ai-assistance",
        body={"requestId": ACTION_ID},
        response={"processItemId": ID},
        result=models.ProcessItemAiAssistance,
    ),
    Case(
        "download_process_item_task_data_webforms_as_document",
        ops.ProcessItemOperations,
        lambda o: b"".join(o.download_process_item_task_data_webforms_as_document(ID, property_path="#/FIELD")),
        "GET",
        f"/process-items/{ID}/task/data/~actions/download-webforms-as-document",
        query={"propertyPath": ["#/FIELD"]},
        response=b"%PDF",
        response_content_type="application/octet-stream",
        result=bytes,
    ),
    # Robot
    Case(
        "find_robots",
        ops.RobotOperations,
        lambda o: o.find_robots(sort="name", tenant_id=TENANT_ID, filter_context=models.RobotFilterContext.READY),
        "GET",
        "/robots",
        query={"size": ["25"], "page": ["0"], "sort": ["name"], "tenantId": [TENANT_ID], "filterContext": ["READY"]},
        response=PAGE,
        result=models.RobotPage,
    ),
    Case(
        "retrieve_robot",
        ops.RobotOperations,
        lambda o: o.retrieve_robot(ID),
        "GET",
        f"/robots/{ID}",
        response={"id": ID, "code": "ROBOT", "name": "Robot"},
        result=models.Robot,
    ),
    Case(
        "download_robot_source_code",
        ops.RobotOperations,
        lambda o: b"".join(o.download_robot_source_code(ID)),
        "GET",
        f"/robots/{ID}/~actions/download-source-code",
        response=b"zip",
        response_content_type="application/octet-stream",
        result=bytes,
    ),
    Case(
        "download_robot_asset",
        ops.RobotOperations,
        lambda o: b"".join(
            o.download_robot_asset(
                ID,
                type=models.RobotAssetType.PYTHON,
                version="3.12",
                platform=models.RobotAssetPlatform.LINUX,
                architecture=models.RobotAssetArchitecture.X86_64,
            )
        ),
        "GET",
        f"/robots/{ID}/~actions/download-asset",
        query={"type": ["PYTHON"], "version": ["3.12"], "platform": ["LINUX"], "architecture": ["X86_64"]},
        response=b"asset",
        response_content_type="application/octet-stream",
        result=bytes,
    ),
    # Tenant
    Case(
        "find_tenants",
        ops.TenantOperations,
        lambda o: o.find_tenants(sort="name", tenant_id=TENANT_ID),
        "GET",
        "/tenants",
        query={"size": ["25"], "page": ["0"], "sort": ["name"], "tenantId": [TENANT_ID]},
        response=PAGE,
        result=models.TenantPage,
    ),
    Case(
        "retrieve_tenant",
        ops.TenantOperations,
        lambda o: o.retrieve_tenant(TENANT_ID),
        "GET",
        f"/tenants/{TENANT_ID}",
        response={"id": TENANT_ID, "name": "Tenant", "plan": "FREE"},
        result=models.Tenant,
    ),
    # Tenant User
    Case(
        "find_tenant_users",
        ops.TenantUserOperations,
        lambda o: o.find_tenant_users(
            sort="name", group_id=ID, group_code="G", email="a@kuflow.com", tenant_id=TENANT_ID
        ),
        "GET",
        "/tenant-users",
        query={
            "size": ["25"],
            "page": ["0"],
            "sort": ["name"],
            "groupId": [ID],
            "groupCode": ["G"],
            "email": ["a@kuflow.com"],
            "tenantId": [TENANT_ID],
        },
        response=PAGE,
        result=models.TenantUserPage,
    ),
    Case(
        "retrieve_tenant_user",
        ops.TenantUserOperations,
        lambda o: o.retrieve_tenant_user(ID),
        "GET",
        f"/tenant-users/{ID}",
        response={"id": ID, "tenantId": TENANT_ID},
        result=models.TenantUser,
    ),
    # Worker
    Case(
        "create_worker",
        ops.WorkerOperations,
        lambda o: o.create_worker(
            models.WorkerCreateParams(
                identity="worker-1",
                task_queue="queue",
                workflow_types=["Wf"],
                activity_types=["Act"],
                hostname="h",
                ip="1.2.3.4",
            )
        ),
        "POST",
        "/workers",
        body={
            "identity": "worker-1",
            "taskQueue": "queue",
            "workflowTypes": ["Wf"],
            "activityTypes": ["Act"],
            "hostname": "h",
            "ip": "1.2.3.4",
        },
        response={"id": ID, "identity": "worker-1", "taskQueue": "queue", "hostname": "h", "ip": "1.2.3.4"},
        result=models.Worker,
    ),
]


@pytest.mark.parametrize("case", CASES, ids=[it.id for it in CASES])
def test_given_an_operation_when_called_then_sends_the_expected_request(stub_client, case: Case):
    if isinstance(case.response, bytes):
        content = case.response
    elif case.response is None:
        content = b""
    else:
        content = json.dumps(case.response).encode()
    kuflow_client, transport = stub_client(
        status_code=case.status, content=content, content_type=case.response_content_type
    )

    result = case.call(case.operations(kuflow_client))

    assert len(transport.requests) == 1
    request = transport.requests[0]
    url = urlparse(request.url)
    assert request.method == case.method
    assert url.path == BASE_PATH + case.path
    if case.query is not None:
        assert parse_qs(url.query) == case.query
    if case.body is not None:
        assert json.loads(request.content) == case.body
    if case.result is None:
        assert result is None
    else:
        assert isinstance(result, case.result)


def test_given_the_operations_when_listed_then_every_one_has_a_request_case():
    tested = {it.id for it in CASES}
    already_tested_elsewhere = {
        "delete_process",
        "find_processes",
        "create_process_action",
        "retrieve_process_action",
        "cancel_process_action",
        "restore_business_artifact",
        "prepare_business_artifact_action_start_process",
        "upload_document",
        "download_document",
        "find_groups",
        "retrieve_kms_key",
    }
    operations = {
        name
        for cls_name in ops.__all__
        for name in vars(getattr(ops, cls_name))
        if not name.startswith("_") and callable(getattr(getattr(ops, cls_name), name))
    }

    assert operations - tested - already_tested_elsewhere == set()

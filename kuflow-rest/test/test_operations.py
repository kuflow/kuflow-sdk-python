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

import io
import json
from urllib.parse import parse_qs, urlparse

from kuflow_rest import models
from kuflow_rest.operations import BusinessArtifactOperations, DocumentOperations, GroupOperations, KmsOperations

from ._stubs import ENDPOINT


BUSINESS_ARTIFACT_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f6"
PROCESS_ID = "0192b7a1-5b1e-7c3d-8e4f-a1b2c3d4e5f8"
PRINCIPAL_ID = "0192b7a1-0000-7000-8000-000000000001"
DOCUMENT_URI = f"ku:process/{PROCESS_ID}/document/0192b7a1-0000-7000-8000-000000000003"
DOCUMENT_REFERENCE = f"kuflow-file:uri={DOCUMENT_URI};type=text/plain;size=5;name=hello.txt;"
FEED_ITEM_THREAD_ID = "019a8c3e-4b2d-7f10-8a3b-5c6d7e8f9a0b"
FEED_ITEM_MESSAGE_ID = "019a8c3e-6d4f-7a21-9b4c-6d7e8f9a0b1c"
FEED_ITEM_TENANT_ID = "00a9f1d4-3698-45a4-951c-66a468846aad"
FEED_ITEM_BUSINESS_ARTIFACT_DEFINITION_ID = "b1c2d3e4-5678-90ab-cdef-1234567890ab"
FEED_ITEM_AUTHOR_ID = "6a7b8c9d-0e1f-4a2b-8c3d-4e5f6a7b8c9d"
FEED_ITEM_THREAD = {
    "id": FEED_ITEM_THREAD_ID,
    "type": "THREAD",
    "tenantId": FEED_ITEM_TENANT_ID,
    "businessArtifactDefinitionRef": {"id": FEED_ITEM_BUSINESS_ARTIFACT_DEFINITION_ID, "code": "ARTIFACT_DEF_CODE"},
    "status": "RUNNING",
    "progress": {"completed": 3, "total": 10},
    "startedAt": "2026-11-16T10:00:00Z",
    "thread": {"title": "Invoice import", "description": "Importing the invoices of **November**"},
    "createdBy": FEED_ITEM_AUTHOR_ID,
    "createdAt": "2026-11-16T09:59:58Z",
    "lastModifiedBy": FEED_ITEM_AUTHOR_ID,
    "lastModifiedAt": "2026-11-16T10:00:00Z",
}
FEED_ITEM_MESSAGE = {
    "id": FEED_ITEM_MESSAGE_ID,
    "type": "MESSAGE",
    "tenantId": FEED_ITEM_TENANT_ID,
    "businessArtifactDefinitionRef": {"id": FEED_ITEM_BUSINESS_ARTIFACT_DEFINITION_ID, "code": "ARTIFACT_DEF_CODE"},
    "businessArtifactFeedItemThreadId": FEED_ITEM_THREAD_ID,
    "status": "COMPLETED",
    "finishedAt": "2026-11-16T10:05:00Z",
    "message": {"text": "Invoice **INV-001** imported", "level": "WARN"},
    "createdBy": FEED_ITEM_AUTHOR_ID,
    "createdAt": "2026-11-16T10:04:58Z",
    "lastModifiedBy": FEED_ITEM_AUTHOR_ID,
    "lastModifiedAt": "2026-11-16T10:05:00Z",
}


def test_given_a_deleted_business_artifact_when_restore_business_artifact_then_posts_the_restore_action(stub_client):
    kuflow_client, transport = stub_client(
        status_code=200,
        content=json.dumps({"objectType": "BUSINESS_ARTIFACT", "id": BUSINESS_ARTIFACT_ID}).encode(),
    )

    business_artifact = BusinessArtifactOperations(kuflow_client).restore_business_artifact(BUSINESS_ARTIFACT_ID)

    assert transport.requests[0].method == "POST"
    assert transport.requests[0].url == f"{ENDPOINT}/business-artifacts/{BUSINESS_ARTIFACT_ID}/~actions/restore"
    assert business_artifact.id == BUSINESS_ARTIFACT_ID


def test_given_a_start_process_action_when_prepare_then_posts_the_params_and_returns_the_metadata(stub_client):
    kuflow_client, transport = stub_client(status_code=200, content=b'{"metadata": {"value": {"FIELD": "value"}}}')
    params = models.BusinessArtifactActionStartProcessPrepareParams(business_artifact_action_definition_code="START")

    prepare = BusinessArtifactOperations(kuflow_client).prepare_business_artifact_action_start_process(
        BUSINESS_ARTIFACT_ID, business_artifact_action_start_process_prepare_params=params
    )

    assert transport.requests[0].method == "POST"
    assert transport.requests[0].url == (
        f"{ENDPOINT}/business-artifacts/{BUSINESS_ARTIFACT_ID}/~actions/prepare-start-process"
    )
    assert json.loads(transport.requests[0].content) == {"businessArtifactActionDefinitionCode": "START"}
    assert isinstance(prepare, models.BusinessArtifactActionStartProcessPrepare)


def test_given_a_document_when_upload_document_then_sends_its_content_and_metadata_for_the_target(stub_client):
    kuflow_client, transport = stub_client(
        status_code=200, content=json.dumps({"documentUri": DOCUMENT_REFERENCE}).encode()
    )
    document = models.Document(file_name="hello.txt", content_type="text/plain", file_content=io.BytesIO(b"hello"))

    document_reference = DocumentOperations(kuflow_client).upload_document(
        document, target_uri=f"ku:process/{PROCESS_ID}"
    )

    request = transport.requests[0]
    query = parse_qs(urlparse(request.url).query)
    assert request.method == "POST"
    assert urlparse(request.url).path == "/v2024-06-14/documents/~actions/upload"
    assert query == {
        "targetUri": [f"ku:process/{PROCESS_ID}"],
        "fileContentType": ["text/plain"],
        "fileName": ["hello.txt"],
    }
    assert request.headers["Content-Type"] == "application/octet-stream"
    assert document_reference.document_uri == DOCUMENT_REFERENCE


def test_given_a_document_uri_when_download_document_then_returns_its_content(stub_client):
    kuflow_client, transport = stub_client(status_code=200, content=b"hello", content_type="application/octet-stream")

    content = b"".join(DocumentOperations(kuflow_client).download_document(document_uri=DOCUMENT_REFERENCE))

    query = parse_qs(urlparse(transport.requests[0].url).query)
    assert transport.requests[0].method == "GET"
    assert urlparse(transport.requests[0].url).path == "/v2024-06-14/documents/~actions/download"
    assert query == {"documentUri": [DOCUMENT_REFERENCE]}
    assert content == b"hello"


def test_given_a_principal_id_when_find_groups_then_sends_it_as_a_single_query_value(stub_client):
    kuflow_client, transport = stub_client(status_code=200, content=b'{"content": [], "metadata": {}}')

    GroupOperations(kuflow_client).find_groups(principal_id=PRINCIPAL_ID, tenant_id="tenant")

    query = parse_qs(urlparse(transport.requests[0].url).query)
    assert query["principalId"] == [PRINCIPAL_ID]
    assert query["tenantId"] == ["tenant"]


def test_given_a_key_id_when_retrieve_kms_key_then_gets_the_key(stub_client):
    kuflow_client, transport = stub_client(status_code=200, content=b'{"id": "key-1", "value": "c2VjcmV0"}')

    kms_key = KmsOperations(kuflow_client).retrieve_kms_key(id="key-1")

    assert transport.requests[0].method == "GET"
    assert transport.requests[0].url == f"{ENDPOINT}/kms/keys/key-1"
    assert kms_key.id == "key-1"


def test_given_thread_create_params_when_create_business_artifact_feed_item_then_sends_them_and_parses_the_thread(
    stub_client,
):
    kuflow_client, transport = stub_client(status_code=201, content=json.dumps(FEED_ITEM_THREAD).encode())
    params = models.BusinessArtifactFeedItemCreateParams(
        id=FEED_ITEM_THREAD_ID,
        type=models.BusinessArtifactFeedItemType.THREAD,
        tenant_id=FEED_ITEM_TENANT_ID,
        business_artifact_definition_code="ARTIFACT_DEF_CODE",
        status=models.BusinessArtifactFeedItemStatus.RUNNING,
        progress=models.BusinessArtifactFeedItemProgress(completed=3, total=10),
        thread=models.BusinessArtifactFeedItemThreadParams(title="Invoice import"),
    )

    feed_item = BusinessArtifactOperations(kuflow_client).create_business_artifact_feed_item(params)

    assert transport.requests[0].method == "POST"
    assert transport.requests[0].url == f"{ENDPOINT}/business-artifact-feed-items"
    assert json.loads(transport.requests[0].content) == {
        "id": FEED_ITEM_THREAD_ID,
        "type": "THREAD",
        "tenantId": FEED_ITEM_TENANT_ID,
        "businessArtifactDefinitionCode": "ARTIFACT_DEF_CODE",
        "status": "RUNNING",
        "progress": {"completed": 3, "total": 10},
        "thread": {"title": "Invoice import"},
    }
    assert feed_item.id == FEED_ITEM_THREAD_ID
    assert feed_item.type == models.BusinessArtifactFeedItemType.THREAD
    assert feed_item.thread.title == "Invoice import"


def test_given_an_already_created_message_when_create_business_artifact_feed_item_then_returns_the_existing_one(
    stub_client,
):
    kuflow_client, transport = stub_client(status_code=200, content=json.dumps(FEED_ITEM_MESSAGE).encode())
    params = models.BusinessArtifactFeedItemCreateParams(
        id=FEED_ITEM_MESSAGE_ID,
        type=models.BusinessArtifactFeedItemType.MESSAGE,
        business_artifact_definition_id=FEED_ITEM_BUSINESS_ARTIFACT_DEFINITION_ID,
        business_artifact_feed_item_thread_id=FEED_ITEM_THREAD_ID,
        message=models.BusinessArtifactFeedItemMessageParams(
            text="Invoice **INV-001** imported", level=models.BusinessArtifactFeedItemMessageLevel.WARN
        ),
    )

    feed_item = BusinessArtifactOperations(kuflow_client).create_business_artifact_feed_item(params)

    assert json.loads(transport.requests[0].content) == {
        "id": FEED_ITEM_MESSAGE_ID,
        "type": "MESSAGE",
        "businessArtifactDefinitionId": FEED_ITEM_BUSINESS_ARTIFACT_DEFINITION_ID,
        "businessArtifactFeedItemThreadId": FEED_ITEM_THREAD_ID,
        "message": {"text": "Invoice **INV-001** imported", "level": "WARN"},
    }
    assert feed_item.id == FEED_ITEM_MESSAGE_ID
    assert feed_item.type == models.BusinessArtifactFeedItemType.MESSAGE
    assert feed_item.business_artifact_feed_item_thread_id == FEED_ITEM_THREAD_ID
    assert feed_item.message.level == models.BusinessArtifactFeedItemMessageLevel.WARN


def test_given_a_business_artifact_feed_item_when_retrieve_business_artifact_feed_item_then_parses_the_body(
    stub_client,
):
    kuflow_client, transport = stub_client(status_code=200, content=json.dumps(FEED_ITEM_THREAD).encode())

    feed_item = BusinessArtifactOperations(kuflow_client).retrieve_business_artifact_feed_item(FEED_ITEM_THREAD_ID)

    assert transport.requests[0].method == "GET"
    assert transport.requests[0].url == f"{ENDPOINT}/business-artifact-feed-items/{FEED_ITEM_THREAD_ID}"
    assert feed_item.id == FEED_ITEM_THREAD_ID
    assert feed_item.tenant_id == FEED_ITEM_TENANT_ID
    assert feed_item.business_artifact_definition_ref.code == "ARTIFACT_DEF_CODE"
    assert feed_item.status == models.BusinessArtifactFeedItemStatus.RUNNING
    assert feed_item.progress.completed == 3
    assert feed_item.progress.total == 10
    assert feed_item.started_at is not None
    assert feed_item.finished_at is None
    assert feed_item.thread.description == "Importing the invoices of **November**"
    assert feed_item.created_by == FEED_ITEM_AUTHOR_ID


def test_given_update_params_when_update_business_artifact_feed_item_then_sends_them_and_parses_the_body(
    stub_client,
):
    kuflow_client, transport = stub_client(status_code=200, content=json.dumps(FEED_ITEM_MESSAGE).encode())
    params = models.BusinessArtifactFeedItemUpdateParams(
        status=models.BusinessArtifactFeedItemStatus.COMPLETED,
        message=models.BusinessArtifactFeedItemMessageParams(
            text="Invoice **INV-001** imported", level=models.BusinessArtifactFeedItemMessageLevel.WARN
        ),
    )

    feed_item = BusinessArtifactOperations(kuflow_client).update_business_artifact_feed_item(
        FEED_ITEM_MESSAGE_ID, business_artifact_feed_item_update_params=params
    )

    assert transport.requests[0].method == "PUT"
    assert transport.requests[0].url == f"{ENDPOINT}/business-artifact-feed-items/{FEED_ITEM_MESSAGE_ID}"
    assert json.loads(transport.requests[0].content) == {
        "status": "COMPLETED",
        "message": {"text": "Invoice **INV-001** imported", "level": "WARN"},
    }
    assert feed_item.id == FEED_ITEM_MESSAGE_ID
    assert feed_item.status == models.BusinessArtifactFeedItemStatus.COMPLETED
    assert feed_item.finished_at is not None

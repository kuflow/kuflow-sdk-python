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

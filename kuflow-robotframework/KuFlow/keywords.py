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
import logging
import os
from typing import Any, Optional
from uuid import UUID

import magic
from robot.api.deco import keyword
from robot.utils import is_dict_like, is_string, type_name

from kuflow_rest import KuBotTokenCredential, KuFlowRestClient, models


class Keywords:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._client: Optional[KuFlowRestClient] = None

    @keyword(tags=("settings",))
    def get_kuBot_token_credential(
        self,
        token: str,
        expires_on: int,
    ) -> KuBotTokenCredential:
        return KuBotTokenCredential(token, expires_on)

    @keyword(tags=("settings",))
    def set_client_authentication(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        credential: Optional[KuBotTokenCredential] = None,
        endpoint: Optional[str] = None,
        allow_insecure_connection: Optional[bool] = None,
    ):
        """Configure the client authentication in order to execute keywords against Rest API.

        Before using any other KuFlow Keyword, this one must be called.

        Example:
        | Set Client Authentication | %{KUFLOW_CLIENT_ID} | %{KUFLOW_CLIENT_SECRET}
        | Set Client Authentication | %{KUFLOW_CLIENT_ID} | %{KUFLOW_CLIENT_SECRET} | %{KUFLOW_API_ENDPOINT}
        =>
        | Set Client Authentication | identifier | token
        | Set Client Authentication | identifier | token | https://api.kuflow.com/v1.0
        """
        if is_string(endpoint) and (endpoint.strip() == "" or endpoint.lower() == "none"):
            endpoint = None

        self._client = KuFlowRestClient(
            client_id=client_id,
            client_secret=client_secret,
            credential=credential,
            endpoint=endpoint,
            allow_insecure_connection=allow_insecure_connection,
        )

    @keyword(tags=("settings",))
    def get_client(self) -> KuFlowRestClient:
        return self._client

    @keyword(tags=("settings",))
    def get_instance(self) -> "Keywords":
        return self

    @keyword(tags=("settings",))
    def convert_to_dictionary_recursively(self, value: dict) -> dict:
        """Converts the given ``value`` to a Python ``dict`` type.

        Mainly useful for converting other mappings to normal dictionaries.
        This includes converting Robot Framework's own ``DotDict`` instances.

        Unlike the `Convert To Dictionary` keyword from Robotframework's Collections library,
        which only converts the first level of the dictionary using "Convert To Dictionary",
        this method performs nested conversion using Json's marshall and unmarshall.
        """
        return json.loads(json.dumps(value))

    @keyword()
    def retrieve_process(self, process_id: UUID) -> models.Process:
        """Allow to get a process by ID.

        Example:
        | RETRIEVE PROCESS | ${PROCESS_ID}
        =>
        | RETRIEVE PROCESS | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec
        """

        return self._client.process.retrieve_process(process_id)

    @keyword()
    def retrieve_process_item(self, process_item_id: UUID) -> models.ProcessItem:
        """Allow to get a process item by ID.

        Example:
        | RETRIEVE PROCESS ITEM | ${PROCESS_ITEM_ID}
        =>
        | RETRIEVE PROCESS ITEM | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec
        """

        return self._client.process_item.retrieve_process_item(process_item_id)

    @keyword()
    def append_process_item_task_log(
        self,
        process_item_id: UUID,
        message: str,
        level: models.ProcessItemTaskLogLevel = models.ProcessItemTaskLogLevel.INFO,
    ) -> models.ProcessItem:
        """Add a log entry to the task

        If the number of log entries is reached, the oldest log entry is removed.
        The level of log can be INFO, WARN or ERROR.

        Example:
        | Append Process Item Task Log | ${PROCESS_ITEM_ID} | ${MESSAGE}
        | Append Process Item Task Log | ${PROCESS_ITEM_ID} | ${MESSAGE} | level=${LEVEL}
        =>
        | Append Process Item Task Log | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | My info message
        | Append Process Item Task Log | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | My warning message | level=WARN
        """
        params = models.ProcessItemTaskAppendLogParams(message=message, level=level)

        return self._client.process_item.append_process_item_task_log(process_item_id, params)

    @keyword()
    def claim_process_item_task(self, process_item_id: UUID) -> models.ProcessItem:
        """Allow to claim a process item task

        Example:
        | CLAIM PROCESS ITEM TASK | ${PROCESS_ITEM_ID}
        =>
        | CLAIM PROCESS ITEM TASK | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec
        """

        return self._client.process_item.claim_process_item_task(process_item_id)

    @keyword()
    def update_process_item_task_data(self, process_item_id: UUID, value: dict[str, Any]) -> models.ProcessItem:
        """Save a JSON value data

        Allows a JSON to be saved in the process item task.

        If previous values already exist in the JSON value, they are replaced by the new values.

        Server-side validations are applied on the saved JSON according to the ones you defined in the schema
        in the process item task definition in KuFlow.

        Example:
        | Update Process Item Task Data | ${PROCESS_ITEM_ID} | ${json_data}
        =>
        | &{json_data}=    Create Dictionary    key1=value1    keu2=value2
        | Update Process Item Task Data | ${PROCESS_ITEM_ID} | ${json_data}
        """
        if not is_dict_like(value):
            raise TypeError(f"Expected argument to be a dict or dict-like, got {type_name(value)} instead.")

        params = models.ProcessItemTaskDataUpdateParams(
            data=models.JsonValue(value=self.convert_to_dictionary_recursively(value))
        )

        return self._client.process_item.update_process_item_task_data(process_item_id, params)

    @keyword()
    def upload_process_item_task_data_document(self, task_id: UUID, path_in_schema: str, path: str) -> str:
        """Upload a JSON Forms value document

        Allows you to upload a document to the referenced task and then include a reference to it
        in the task's JSON Forms.

        You must provide the path within the JSON schema that defines the document you wish to upload.
        This schema is found in your task definition in KuFlow. For example, given this schema:

        {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "format": "kuflow-file",
                    "accept": "image/*,application/pdf,.pdf",
                    "maxSize": 20000000
                }
            }
        }

        The path is as follows: #/properties/file

        Note that in RobotFramework, the hash indicates a comment, so you should escape it

        Example:
        | Upload Process Item Task Data Document | ${PROCESS_ITEM_ID} | ${PATH_IN_SCHEMA} | ${PATH}
        =>
        | ${document_reference}=
        | ... Upload Json Forms Value document | ${PROCESS_ITEM_ID} | \\#/properties/file | hello.jpg
        | &{json_data}=    Create Dictionary    my_file=${document_reference}
        | Update Process Item Task Data    ${KUFLOW_TASK_ID}    ${json_data}
        """

        file_name = os.path.basename(path)
        file = open(path, "rb")
        content_type = magic.from_file(path, mime=True)

        file = models.Document(
            file_mame=file_name,
            content_type=content_type,
            file_content=file,
        )

        response = self._client.process_item.upload_process_item_task_data_document(
            id=task_id, file=file, schema_path=path_in_schema
        )

        return response.value

    @keyword()
    def convert_json_string_to_object(self, json_string):
        """Convert JSON String To Object

        Given a JSON string as argument, return new JSON object

        Example:
        | ${json_object}=  |  Convert JSON String To Object | ${json_string} |
        =>
        | ${json_string}=    catenate
        | ...  {
        | ...    "key1": "10",
        | ...    "key2": {
        | ...            "subkey1": "My value"
        | ...          }
        | ...  }
        | ${json_object}=  |  Convert JSON String To Object | ${json_string} |
        """
        return json.loads(json_string)

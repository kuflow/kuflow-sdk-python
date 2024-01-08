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
from typing import Optional, Union
from uuid import UUID

import magic
from robot.api.deco import keyword
from robot.utils import is_dict_like, is_list_like, is_number, is_string, type_name

from kuflow_rest import KuFlowRestClient, models


class Keywords:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._client = None

    @keyword(tags=("settings",))
    def set_client_authentication(
        self,
        client_id: str,
        client_secret: str,
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
    def append_log_message(self, task_id: UUID, message: str, level=models.LogLevel.INFO) -> models.Task:
        """Add a log entry to the task

        If the number of log entries is reached, the oldest log entry is removed.
        The level of log can be INFO, WARN or ERROR.

        Example:
        | Append Log Message | ${TASK_ID} | ${MESSAGE}
        | Append Log Message | ${TASK_ID} | ${MESSAGE} | level=${LEVEL}
        =>
        | Append Log Message | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | My info message
        | Append Log Message | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | My warning message | level=WARN
        """
        log = models.Log(message=message, level=level)

        return self._client.task.actions_task_append_log(task_id, log)

    @keyword()
    def claim_task(self, task_id: UUID) -> models.Task:
        """Allow to claim a task

        Example:
        | CLAIM TASK | ${TASK_ID}
        =>
        | CLAIM TASK | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec
        """

        return self._client.task.actions_task_claim(task_id)

    @keyword()
    def retrieve_process(self, process_id: UUID) -> models.Task:
        """Allow to get a process by ID.

        Example:
        | RETRIEVE PROCESS | ${PROCESS_ID}
        =>
        | RETRIEVE PROCESS | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec
        """

        return self._client.process.retrieve_process(process_id)

    @keyword()
    def retrieve_task(self, task_id: UUID) -> models.Task:
        """Allow to get a task by ID.

        Example:
        | RETRIEVE TASK | ${TASK_ID}
        =>
        | RETRIEVE TASK | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec
        """

        return self._client.task.retrieve_task(task_id)

    @keyword()
    def save_element_document(self, task_id: UUID, code: str, path: str, id: UUID = None, valid=True) -> models.Task:
        """Save a element of type document

        Allow to save an element document uploading the content.

        If it is a multiple element, and the documentId does not exist or is empty, the document will be added to
        the element.
        If the element already exists (the id referenced in the body corresponds to an existing one), it updates it.

        You also can optionally mark the document as invalid.

        Example:
        | Save Element Document | ${TASK_ID} | ${CODE} | ${PATH}
        =>
        | Save Element Document | ${TASK_ID} | ELEMENT_KEY | hello.jpg
        | Save Element Document | ${TASK_ID} | ELEMENT_KEY | hello.jpg | ${False}
        | Save Element Document | ${TASK_ID} | ELEMENT_KEY | hello.jpg | a05f197f-a50a-46d5-bdec-29a0c020f0d7
        | Save Element Document | ${TASK_ID} | ELEMENT_KEY | hello.jpg | a05f197f-a50a-46d5-bdec-29a0c020f0d7 | ${False}
        """

        file_name = os.path.basename(path)
        file = open(path, "rb")
        content_type = magic.from_file(path, mime=True)

        file = models.Document(
            file_mame=file_name,
            content_type=content_type,
            file_content=file,
        )
        command = models.TaskSaveElementValueDocumentCommand(
            element_definition_code=code, element_value_id=id, element_value_valid=valid
        )

        return self._client.task.actions_task_save_element_value_document(id=task_id, file=file, command=command)

    @keyword()
    def delete_element_document(self, task_id: UUID, id: UUID):
        """Delete an element document value

        Allow to delete a specific document from an element of document type using its Id.

        Note: If it is a multiple item, it will only delete the specified document. If it is a single element,
        in addition to the document, it will also delete the element.

        Example:
        | Delete Element Document | ${TASK_ID} | ${ID}
        =>
        | Delete Element Document | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ac951e9f-c194-445b-9eec-4a800b25fb56
        """

        command = models.TaskDeleteElementValueDocumentCommand(document_id=str(id))

        self._client.task.actions_task_delete_element_value_document(id=task_id, command=command)

    @keyword()
    def save_element(self, task_id: UUID, code: str, *value, valid=True) -> models.Task:
        """Save a element

        Allow to save an element i.e., a field, a decision, a form, a principal or document.

        If values already exist for the provided element code, it replaces them with the new ones,
        otherwise it creates them.
        The values of the previous elements that no longer exist will be deleted.
        To remove an element, use the appropriate API method.

        Type of arguments in keywords and KuFlow elements:
            - String:
                By default, plain argument in keywords are of type String.

            - Number:
                You can use the built-in keywords 'Convert To Integer', 'Convert To Number' or others
                to pass a numeric type element.

        Object Elements (aka Forms Elements in KuFlow):
            You must pass an argument of type dictionary. You can use the built-in keyword
            Create Dictionary or others as utilities.

        Principal Elements:
            The keyword 'Convert To Element Value Principal Item' will allow you to create a Principal
            object that you can use as an argument.

        Document Elements:
            To save a document you need to pass a document reference using the 'id' attribute.
            To upload a new file, please use the 'Save Element Document' keyword.
            The keyword 'Convert To Element Value Document Item' will allow you to create a Principal
            object that you can use as an argument. The identifier of the documents follows the following
            format: ku:task/{taskId}/element-value/{elementValueId}

        Multivalues elements:
            For those elements that have been defined as multiple, you can pass a variable list
            of arguments to the keyword.

        Valid flag for elements:
            When saving an element, it is possible to specify if its value is valid or not,
            which allows it to be shown in the KuFlow UI as a validated element or not. To do this
            you must use the Valid=Boolean parameter. Note that in RobotFramework format the default
            type of parameters is String, so you must write Valid=${False}. By default, all items
            are valid when saved. Similarly, for multi-evaluated elements, the value of the "valid"
            parameter applies to all values.

        Example:
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE}
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE} | ${VALID}
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE_1} | ${VALUE_2} | ${VALUE_3}
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE_1} | ${VALUE_2} | ${VALUE_3} | ${VALID}
        =>
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | Value
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | Value | ${False}
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | Value 1 | Value 2 | Value 3 | ${False}
        |
        | ${result} = Convert To Integer    123
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | ${result}
        |
        | ${result_one} = Convert To Integer | 123
        | ${result_two} = Convert To Number |  123.123
        | Save Element | ${TASK_ID} | FIELD | ${result_one} | ${result_two}
        |
        | ${result} = Convert To Principal Item    7dd16e94-2dac-4fca-931e-c2505baa695c
        | Save Element | ${TASK_ID} | FIELD | ${result}
        |
        | &{result_one} = Create Dictionary | one_key=My Example Value One | two_key=2
        | &{result_two} = Create Dictionary | a_key=My Example Value A | b_key=B
        | Save Element | ${TASK_ID} | FIELD | ${result_one} | ${result_two}
        |
        | ${result} = Convert To Document Item From Uri
        | ...   ku:task/acdca56f-b8aa-46c8-9055-8ee52810a4a9/element-value/a05f197f-a50a-46d5-bdec-29a0c020f0d7
        | Save Element | ${TASK_ID} | FIELD | ${result}
        """
        if not is_list_like(value):
            raise TypeError("Expected argument to be a list or list-like, " "got %s instead." % (type_name(value)))

        target = []
        for v in value:
            element = None

            if is_string(v):
                element = models.TaskElementValueString(value=v, valid=valid)
            elif is_number(v):
                element = models.TaskElementValueNumber(value=v, valid=valid)
            elif isinstance(v, models.TaskElementValuePrincipalItem):
                element = models.TaskElementValuePrincipal(value=v, valid=valid)
            elif isinstance(v, models.TaskElementValueDocumentItem):
                element = models.TaskElementValueDocument(value=v, valid=valid)
            elif is_dict_like(v):
                element = models.TaskElementValueObject(value=self.convert_to_dictionary_recursively(v), valid=valid)
            else:
                element = models.TaskElementValueString(value=v, valid=valid)

            target.append(element)

        command = models.TaskSaveElementCommand(element_definition_code=code, element_values=target)

        return self._client.task.actions_task_save_element(id=task_id, command=command)

    @keyword()
    def delete_element(self, task_id: UUID, code: str) -> models.Task:
        """Delete an element by code

        Allow to delete task element by specifying the item definition code.

        Remove all values of the selected element.

        Example:
        | Delete Element | ${TASK_ID} | ${CODE}
        =>
        | Delete Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY
        """

        command = models.TaskDeleteElementCommand(element_definition_code=code)

        return self._client.task.actions_task_delete_element(id=task_id, command=command)

    @keyword()
    def convert_to_principal_item(
        self, id: UUID, type: Union[str, "models.PrincipalType"]
    ) -> models.TaskElementValuePrincipalItem:
        """Convert to element value principal item

        Given an id of a Principal, create an item that represents a reference to the Principal. Then can be used
        as a value in the keyword 'Save Element'. The principal ID can be obtained through some api methods such
        as "Find all accessible Principals" or implicitly in some resources such as the Initiator of a process
        or the Owner of a task.

        Example:
        | Convert To Principal Item  | ${PRINCIPAL_ID} | ${PRINCIPAL_TYPE}
        =>
        | Convert To Principal Item  | 7dd16e94-2dac-4fca-931e-c2505baa695c | USER
        """

        return models.TaskElementValuePrincipalItem(id=str(id), type=type)

    @keyword()
    def convert_to_document_item_from_uri(self, uri: str) -> models.TaskElementValueDocumentItem:
        """Convert to element value principal item

        Given an id of a Document or the Reference of a Document, create an item that represents a reference to the
        Document element and can be used. Then can be used as a value in the keyword 'Save Element'.

        Example:
        | Convert To Document Item From Uri  | ${ID}
        | Convert To Document Item From Uri  | ${ID} | ${DOCUMENT_URI}
        =>
        | Convert To Document Item From Uri
        | ...   ku:task/acdca56f-b8aa-46c8-9055-8ee52810a4a9/element-value/a05f197f-a50a-46d5-bdec-29a0c020f0d7
        """

        return models.TaskElementValueDocumentItem(uri=uri)

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

    @keyword()
    def save_json_forms_value_data(self, task_id: UUID, value) -> models.Task:
        """Save a JSON Forms value data

        Allows a JSON Forms to be saved in the task.

        If previous values already exist in the JSON Forms value, they are replaced by the new values.

        Server-side validations are applied on the saved JSON Forms according to the ones you defined in the schema
        in the task definition in KuFlow.

        Example:
        | Save Json Forms Value Data    | ${KUFLOW_TASK_ID} | ${json_form_data}
        =>
        | &{json_form_data}=    Create Dictionary    key1=value1    keu2=value2
        | Save Json Forms Value Data    | ${TASK_ID}    | ${json_form_data}
        """
        if not is_dict_like(value):
            raise TypeError("Expected argument to be a dict or dict-like, " "got %s instead." % (type_name(value)))

        command = models.TaskSaveJsonFormsValueDataCommand(data=self.convert_to_dictionary_recursively(value))

        return self._client.task.actions_task_save_json_forms_value_data(id=task_id, command=command)

    @keyword()
    def upload_json_forms_value_document(self, task_id: UUID, path_in_schema: str, path: str) -> str:
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
        | Upload Json Forms Value document    | ${KUFLOW_TASK_ID} | ${PATH_IN_SCHEMA} | ${PATH}
        =>
        | ${document_reference}=
        | ... Upload Json Forms Value document    | ${KUFLOW_TASK_ID} | \\#/properties/file | hello.jpg
        | &{json_form_data}=    Create Dictionary    my_file=${document_reference}
        | Save Json Forms Value Data    ${KUFLOW_TASK_ID}    ${json_form_data}
        """

        file_name = os.path.basename(path)
        file = open(path, "rb")
        content_type = magic.from_file(path, mime=True)

        file = models.Document(
            file_mame=file_name,
            content_type=content_type,
            file_content=file,
        )
        command = models.TaskSaveJsonFormsValueDocumentRequestCommand(schema_path=path_in_schema)

        response = self._client.task.actions_task_save_json_forms_value_document(id=task_id, file=file, command=command)

        return response.value

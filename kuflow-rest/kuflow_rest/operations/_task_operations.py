# coding=utf-8
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


from typing import Any, Iterator, List, Optional, Union

from .. import models as _models
from .._generated import KuFlowRestClient as KuFlowRestClientGenerated


class TaskOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`task` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def find_tasks(
        self,
        size: int = 25,
        page: int = 0,
        sort: Optional[Union[str, List[str]]] = None,
        process_id: Optional[Union[str, List[str]]] = None,
        state: Optional[Union[_models.TaskState, List[_models.TaskState]]] = None,
        task_definition_code: Optional[Union[str, List[str]]] = None,
        **kwargs: Any,
    ) -> _models.TaskPage:
        """Find all accessible Tasks.

        List all Tasks that have been created and the credentials has access.

        Available sort query values: id, createdAt, lastModifiedAt, claimedAt, completedAt,
        cancelledAt.

        :keyword size: The number of records returned within a single API call. Default value is 25.
        :type size: int
        :keyword page: The page number of the current page in the returned records, 0 is the first page.
                       Default value is 0.
        :type page: int
        :keyword sort: Sorting criteria in the format: property{,asc|desc}. Example: createdAt,desc
                       Default sort order is ascending. Multiple sort criteria are supported.
                       Please refer to the method description for supported properties. Default value is None.
        :type sort: list[str]
        :keyword process_id: Filter by an array of process ids. Default value is None.
        :type process_id: list[str]
        :keyword state: Filter by an array of task states. Default value is None.
        :type state: list[str or ~kuflow.rest.models.TaskState]
        :keyword task_definition_code: Filter by an array of task definition codes. Default value is None.
        :type task_definition_code: list[str]
        :return: TaskPage
        :rtype: ~kuflow.rest.models.TaskPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if sort is not None and isinstance(sort, str):
            sort = [sort]
        if process_id is not None and isinstance(process_id, str):
            process_id = [process_id]
        if state is not None and isinstance(state, _models.TaskState):
            state = [state]
        if task_definition_code is not None and isinstance(task_definition_code, str):
            task_definition_code = [task_definition_code]

        return self._kuflow_client.task.find_tasks(
            size=size,
            page=page,
            sort=sort,
            process_id=process_id,
            state=state,
            task_definition_code=task_definition_code,
            **kwargs,
        )

    def create_task(self, task: _models.Task, **kwargs: Any) -> _models.Task:
        """Create a new Task in the selected Process.

        Create a Task and optionally fill its elements. We can fill in any type of element except
        documents.

        If you want to add document type elements, you can pass a reference to an existing document
        type element indicating its 'uri'. This will copy that document into the element. In case you
        want to add a new document, please use the corresponding API method.

        If you want that the task created is claimed you can a valid owner using the following options:


        * If you know the ``principal ID`` you can assign it to ``owner.id``
        * If you know the ``user ID`` you can assign it to ``owner.user.id``
        * If you know the ``user email`` you can assign it to ``owner.user.email``
        * If you know the ``application ID`` you can assign it to ``owner.application.id``

        If you want the method to be idempotent, please specify the ``id`` field in the request body.

        :param task: Task to be created. Required.
        :type task: ~kuflow.rest.models.Task
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.create_task(task=task, **kwargs)

    def retrieve_task(self, id: str, **kwargs: Any) -> _models.Task:
        """Get a task given it ID.

        Allow to get a task by ID.

        :param id: The resource ID. Required.
        :type id: str
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.retrieve_task(id=id, **kwargs)

    def actions_task_claim(self, id: str, **kwargs: Any) -> _models.Task:
        """Claim a task.

        Allow to claim a task.

        :param id: The resource ID. Required.
        :type id: str
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_claim(id=id, **kwargs)

    def actions_task_assign(
        self, id: str, command: _models.TaskAssignCommand, **kwargs: Any
    ) -> _models.Task:
        """Assign a task.

        Allow to assign a task to a user or application. Only one option will be necessary.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to change the task owner. Required.
        :type command: ~kuflow.rest.models.TaskAssignCommand
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_assign(
            id=id, command=command, **kwargs
        )

    def actions_task_save_element(
        self, id: str, command: _models.TaskSaveElementCommand, **kwargs: Any
    ) -> _models.Task:
        """Save an element.

        Allow to save an element i.e., a field, a decision, a form, a principal or document.

        In the case of document type elements, this method only allows references to be made to other
        existing document type elements for the purpose of copying that file into the element. To do
        this you need to pass a reference to the document using the 'uri' attribute. In case you want
        to add a new document, please use the corresponding API method. If values already exist for the
        provided element code, it replaces them with the new ones, otherwise it creates them. The
        values of the previous elements that no longer exist will be deleted. To remove an element, use
        the appropriate API method.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to save an element. Required.
        :type command: ~kuflow.rest.models.TaskSaveElementCommand
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_save_element(
            id=id, command=command, **kwargs
        )

    def actions_task_save_element_value_document(
        self,
        id: str,
        file: _models.Document,
        command: _models.TaskSaveElementValueDocumentCommand,
        **kwargs: Any,
    ) -> _models.Task:
        """Save an element document.

        Allow to save an element document uploading the content.

        If it is a multiple element, and the ID referenced in the body does not exist or is empty, the
        document will be added to the element. If the element already exists (the ID referenced in the
        body corresponds to an existing one), it updates it.

        :param id: The resource ID. Required.
        :type id: str
        :param file: Document to save. Required.
        :type file: ~kuflow.rest.models.Document
        :param command: Command info. Required.
        :type command: ~kuflow.rest.models.TaskSaveElementValueDocumentCommand
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_save_element_value_document(
            id=id,
            file=file.file_content,
            file_content_type=file.content_type,
            file_name=file.file_mame,
            element_definition_code=command.element_definition_code,
            element_value_id=command.element_value_id,
            element_value_valid=command.element_value_valid,
            **kwargs,
        )

    def actions_task_delete_element(
        self, id: str, command: _models.TaskDeleteElementCommand, **kwargs: Any
    ) -> _models.Task:
        """Delete an element by code.

        Allow to delete task element by specifying the item definition code.

        Remove all the element values.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to delete an element. Required.
        :type command: ~kuflow.rest.models.TaskDeleteElementCommand
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_delete_element(
            id=id, command=command, **kwargs
        )

    def actions_task_delete_element_value_document(
        self,
        id: str,
        command: _models.TaskDeleteElementValueDocumentCommand,
        **kwargs: Any,
    ) -> _models.Task:
        """Delete an element document value.

        Allow to delete a specific document from an element of document type using its id.

        Note: If it is a multiple item, it will only delete the specified document. If it is a single
        element, in addition to the document, it will also delete the element.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to delete a document element value. Required.
        :type command: ~kuflow.rest.models.TaskDeleteElementValueDocumentCommand
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_delete_element_value_document(
            id=id, command=command, **kwargs
        )

    def actions_task_download_element_value_document(
        self, id: str, document_id: str, **kwargs: Any
    ) -> Iterator[bytes]:
        """Download document.

        Given a task, download a document from an element of document type.

        :param id: The resource ID. Required.
        :type id: str
        :keyword document_id: Document ID to download. Required.
        :type document_id: str
        :return: Iterator of the response bytes
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_download_element_value_document(
            id=id, document_id=document_id, **kwargs
        )

    def actions_task_download_element_value_rendered(
        self, id: str, element_definition_code: str, **kwargs: Any
    ) -> Iterator[bytes]:
        """Download a Form rendered as PDF or Zip of PDFs (when the element is multiple).

        Given a task, generate a PDF from a Form type element with the data filled in, if any. If there
        are multiple form values, they are packed into a ZIP.

        Important!: To use this feature, please contact to kuflow@kuflow.com.

        :param id: The resource ID. Required.
        :type id: str
        :param element_definition_code: Element definition code of a Form Element to download.
        :type element_definition_code: str
        :return: Iterator of the response bytes
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_download_element_value_rendered(
            id=id, element_definition_code=element_definition_code, **kwargs
        )

    def actions_task_save_json_forms_value_data(
        self,
        id: str,
        command: _models.TaskSaveJsonFormsValueDataCommand,
        **kwargs: Any,
    ) -> _models.Task:
        """Save JSON data.

        Allow to save a JSON data validating that the data follow the related schema. If the data is
        invalid, then
        the json form is marked as invalid.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to save the JSON value. Required.
        :type command: ~kuflow.rest.models.TaskSaveJsonFormsValueDataCommand
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_save_json_forms_value_data(
            id=id, command=command, **kwargs
        )

    def actions_task_save_json_forms_value_document(
        self,
        id: str,
        file: _models.Document,
        command: _models.TaskSaveJsonFormsValueDocumentRequestCommand,
        **kwargs: Any,
    ) -> _models.TaskSaveJsonFormsValueDocumentResponseCommand:
        """Save a JSON Forms document.

        Save a document in the task to later be linked into the JSON data.

        :param id: The resource ID. Required.
        :type id: str
        :param file: Document to save. Required.
        :type file: ~kuflow.rest.models.Document
        :param command: Command to save the JSON value. Required.
        :type command: ~kuflow.rest.models.TaskSaveJsonFormsValueDataCommand
        :return: TaskSaveJsonFormsValueDocumentResponseCommand
        :rtype: ~kuflow.rest.models.TaskSaveJsonFormsValueDocumentResponseCommand
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_save_json_forms_value_document(
            id=id,
            file=file.file_content,
            file_content_type=file.content_type,
            file_name=file.file_mame,
            schema_path=command.schema_path,
            **kwargs,
        )

    def actions_task_download_json_forms_value_document(
        self, id: str, *, document_uri: str, **kwargs: Any
    ) -> Iterator[bytes]:
        """Download document.

        Given a task, download a document from a json form data.

        :param id: The resource ID. Required.
        :type id: str
        :param document_uri: Document URI to download. Required.
        :type document_uri: str
        :return: Iterator of the response bytes
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_download_json_forms_value_document(
            id=id,
            document_uri=document_uri,
            **kwargs,
        )

    def actions_task_complete(self, id: str, **kwargs: Any) -> _models.Task:
        """Complete a task.

        Allow to complete a claimed task by the principal.

        :param id: The resource ID. Required.
        :type id: str
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_complete(id=id, **kwargs)

    def actions_task_append_log(
        self, id: str, log: _models.Log, **kwargs: Any
    ) -> _models.Task:
        """Append a log to the task.

        A log entry is added to the task. If the number of log entries is reached, the oldest log entry
        is removed.

        :param id: The resource ID. Required.
        :type id: str
        :param log: Log to be created. Required.
        :type log: ~kuflow.rest.models.Log
        :return: Task
        :rtype: ~kuflow.rest.models.Task
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.task.actions_task_append_log(
            id=id, log=log, **kwargs
        )

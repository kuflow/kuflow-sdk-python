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

from collections.abc import Iterator
from typing import Any, Optional, Union

from .. import models as _models
from .._generated import KuFlowRestClient as KuFlowRestClientGenerated


class ProcessItemOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`task` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def find_process_items(
        self,
        size: int = 25,
        page: int = 0,
        sort: Optional[Union[str, list[str]]] = None,
        process_id: Optional[Union[str, list[str]]] = None,
        type: Optional[list[_models.ProcessItemType]] = None,
        task_state: Optional[Union[_models.ProcessItemTaskState, list[_models.ProcessItemTaskState]]] = None,
        process_item_definition_code: Optional[Union[str, list[str]]] = None,
        tenant_id: Optional[Union[str, list[str]]] = None,
        **kwargs: Any,
    ) -> _models.ProcessItemPage:
        """Find all accessible Process Items.

        List all Process Items that have been created and the credentials has access.

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
        :keyword type: Filter by an array of process item types. Default value is None.
        :type type: list[~kuflow.rest.models.ProcessItemType]
        :keyword task_state: Filter by an array of process item task states. Default value is None.
        :type task_state: list[~kuflow.rest.models.ProcessItemTaskState]
        :keyword process_item_definition_code: Filter by an array of process item definition codes.
                                               Default value is None.
        :type process_item_definition_code: list[str]
        :keyword tenant_id: Filter process items that exists in one of tenant ids. Default value is None.
        :type tenant_id: Optional[Union[str, List[str]]]
        :return: ProcessItemPage
        :rtype: ~kuflow.rest.models.ProcessItemPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if sort is not None and isinstance(sort, str):
            sort = [sort]

        if process_id is not None and isinstance(process_id, str):
            process_id = [process_id]

        if type is not None and isinstance(type, _models.ProcessItemType):
            type = [type]

        if task_state is not None and isinstance(task_state, _models.ProcessItemTaskState):
            task_state = [task_state]

        if process_item_definition_code is not None and isinstance(process_item_definition_code, str):
            process_item_definition_code = [process_item_definition_code]

        if tenant_id is not None and isinstance(tenant_id, str):
            tenant_id = [tenant_id]

        return self._kuflow_client.process_item.find_process_items(
            size=size,
            page=page,
            sort=sort,
            process_id=process_id,
            type=type,
            task_state=task_state,
            process_item_definition_code=process_item_definition_code,
            tenant_id=tenant_id,
            **kwargs,
        )

    def create_process_item(
        self, process_item_create_params: _models.ProcessItemCreateParams, **kwargs: Any
    ) -> _models.ProcessItem:
        """Create a new Process Item in the selected Process.

        Create a Process Item and optionally fill its value.

        If you want to add document type elements, you can pass a reference to an existing document
        type element
        indicating its 'uri'. This will copy that document into the element. In case you want to add a
        new document,
        please use the corresponding API method.

        If you want the method to be idempotent, please specify the ``id`` field in the request body.

        :param process_item_create_params: Task to be created. Required.
        :type process_item_create_params: ~kuflow.rest.models.ProcessItem
        :return: ProcessItem
        :rtype: ~kuflow.rest.models.ProcessItem
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.create_process_item(
            process_item_create_params=process_item_create_params, **kwargs
        )

    def retrieve_process_item(self, id: str, **kwargs: Any) -> _models.ProcessItem:
        """Get a process item given it ID.

        Allow to get a process item by ID.

        :param id: The resource ID. Required.
        :type id: str
        :return: ProcessItem
        :rtype: ~kuflow.rest.models.ProcessItem
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.retrieve_process_item(id=id, **kwargs)

    def claim_process_item_task(self, id: str, **kwargs: Any) -> _models.ProcessItem:
        """Claim a process item task.

        Allow to claim a task.

        :param id: The resource ID. Required.
        :type id: str
        :return: ProcessItem
        :rtype: ~kuflow.rest.models.ProcessItem
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.claim_process_item_task(id=id, **kwargs)

    def assign_process_item_task(
        self, id: str, process_item_task_assign_params: _models.ProcessItemTaskAssignParams, **kwargs: Any
    ) -> _models.ProcessItem:
        """Assign a process item task.

        Allow to assign a process item task to a user or application. Only one option will be
        necessary.

        :param id: The resource ID. Required.
        :type id: str
        :param process_item_task_assign_params: Params to change the task owner. Required.
        :type process_item_task_assign_params: ~kuflow.rest.models.ProcessItemTaskAssignParams
        :return: ProcessItem
        :rtype: ~kuflow.rest.models.ProcessItem
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.assign_process_item_task(
            id=id, process_item_task_assign_params=process_item_task_assign_params, **kwargs
        )

    def complete_process_item_task(self, id: str, **kwargs: Any) -> _models.ProcessItem:
        """Complete a process item task.

        Allow to complete a claimed task by the principal.

        :param id: The resource ID. Required.
        :type id: str
        :return: ProcessItem
        :rtype: ~kuflow.rest.models.ProcessItem
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.complete_process_item_task(id=id, **kwargs)

    def append_process_item_task_log(
        self, id: str, process_item_task_append_log_params: _models.ProcessItemTaskAppendLogParams, **kwargs: Any
    ) -> _models.ProcessItem:
        """Append a log to the process item task.

        A log entry is added to the task. If the number of log entries is reached, the oldest log entry
        is removed.


        :param id: The resource ID. Required.
        :type id: str
        :param process_item_task_append_log_params: Log to be created. Required.
        :type process_item_task_append_log_params: ~kuflow.rest.models.Log
        :return: ProcessItem
        :rtype: ~kuflow.rest.models.ProcessItem
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.append_process_item_task_log(
            id=id, process_item_task_append_log_params=process_item_task_append_log_params, **kwargs
        )

    def update_process_item_task_data(
        self, id: str, process_item_task_data_update_params: _models.ProcessItemTaskDataUpdateParams, **kwargs: Any
    ) -> _models.ProcessItem:
        """Save JSON data.

        Allow to save a JSON data validating that the data follow the related schema. If the data is
        invalid, then
        the json form is marked as invalid.

        :param id: The resource ID. Required.
        :type id: str
        :param process_item_task_data_update_params: Params to update a process item task data. Required.
        :type process_item_task_data_update_params: ~kuflow.rest.models.ProcessItemSaveElementCommand
        :return: ProcessItem
        :rtype: ~kuflow.rest.models.ProcessItem
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.update_process_item_task_data(
            id=id, process_item_task_data_update_params=process_item_task_data_update_params, **kwargs
        )

    def patch_process_item_task_data(
        self, id: str, json_patch: list[_models.JsonPatchOperation], **kwargs: Any
    ) -> _models.ProcessItem:
        """Save JSON data.

        Allow to save a JSON data validating that the data follow the related schema. If the data is
        invalid, then
        the json form is marked as invalid.

        :param id: The resource ID. Required.
        :type id: str
        :param json_patch: Params to update a process item task data. Required.
        :type json_patch: List[~kuflow.rest.models.JsonPatchOperation]
        :return: ProcessItem
        :rtype: ~kuflow.rest.models.ProcessItem
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.patch_process_item_task_data(id=id, json_patch=json_patch, **kwargs)

    def download_process_item_task_data_webforms_as_document(
        self, id: str, property_path: str, **kwargs: Any
    ) -> Iterator[bytes]:
        """Download a Form rendered as PDF or Zip of PDFs (when the element is multiple).

        Given a task, generate a PDF from a Form type element with the data filled in, if any. If there
        are multiple form values, they are packed into a ZIP.

        Important!: To use this feature, please contact to kuflow@kuflow.com.

        :param id: The resource ID. Required.
        :type id: str
        :keyword property_path: JSON pointer to the property with the error. See:
         https://datatracker.ietf.org/doc/html/rfc6901

         ie: /user/name or /users/1/name. Required.
        :type property_path: str
        :return: Iterator of the response bytes
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process_item.download_process_item_task_data_webforms_as_document(
            id=id, property_path=property_path, **kwargs
        )

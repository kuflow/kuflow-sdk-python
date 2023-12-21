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

from typing import Any, List, Optional, Union

from .. import models as _models
from .._generated import KuFlowRestClient as KuFlowRestClientGenerated


class ProcessOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`process` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def find_processes(
        self,
        size: int = 25,
        page: int = 0,
        sort: Optional[Union[str, List[str]]] = None,
        **kwargs: Any,
    ) -> _models.ProcessPage:
        """Find all accessible Processes.

        List all the Processes that have been created and the credentials has access.

        Available sort query values: id, createdAt, lastModifiedAt.

        :keyword size: The number of records returned within a single API call. Default value is 25.
        :type size: int
        :keyword page: The page number of the current page in the returned records, 0 is the first page.
                       Default value is 0.
        :type page: int
        :keyword sort: Sorting criteria in the format: property{,asc|desc}. Example: createdAt,desc

                       Default sort order is ascending. Multiple sort criteria are supported.

                       Please refer to the method description for supported properties. Default value is None.
        :type sort: Optional[Union[str, List[str]]]
        :return: ProcessPage
        :rtype: ~kuflow.rest.models.ProcessPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if sort is not None and isinstance(sort, str):
            sort = [sort]

        return self._kuflow_client.process.find_processes(
            size=size, page=page, sort=sort, **kwargs
        )

    def create_process(
        self, process: _models.Process, **kwargs: Any
    ) -> _models.Process:
        """Create a new process.

        Creates a process. This option has direct correspondence to the action of starting a process in
        the Kuflow GUI.

        When a process is created, the current user is assigned as the process initiator, if you want
        to change it, you can pass a valid initiator using the following options:


        * If you know the ``principal ID`` you can assign it to ``initiator.id``
        * If you know the ``user ID`` you can assign it to ``initiator.user.id``
        * If you know the ``user email`` you can assign it to ``initiator.user.email``
        * If you know the ``application ID`` you can assign it to ``initiator.application.id``

        If you want the method to be idempotent, please specify the ``id`` field in the request body.

        :param process: Process to create. Required.
        :type process: ~kuflow.rest.models.Process
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.create_process(process=process, **kwargs)

    def retrieve_process(self, id: str, **kwargs: Any) -> _models.Process:
        """Get a Process by ID.

        Returns the requested Process when has access to do it.

        :param id: The resource ID. Required.
        :type id: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.retrieve_process(id=id, **kwargs)

    def actions_process_change_initiator(
        self, id: str, command: _models.ProcessChangeInitiatorCommand, **kwargs: Any
    ) -> _models.Process:
        """Change process initiator.

        Change the current initiator of a process.

        Allows you to choose a user (by email or principal identifier) or an application (principal
        identifier).
        Only one option will be necessary.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to change the process initiator. Required.
        :type command: ~kuflow.rest.models.ProcessChangeInitiatorCommand
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.actions_process_change_initiator(
            id=id, command=command, **kwargs
        )

    def actions_process_save_element(
        self, id: str, command: _models.ProcessSaveElementCommand, **kwargs: Any
    ) -> _models.Process:
        """Save a process element, aka: metadata.

        Allow to save an element.

        If values already exist for the provided element code, it replaces them with the new ones,
        otherwise it creates them. The values of the previous elements that no longer exist will be
        deleted.

        If the process is already finished the invocations fails with an error.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to save an element. Required.
        :type command: ~kuflow.rest.models.ProcessSaveElementCommand
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.actions_process_save_element(
            id=id, command=command, **kwargs
        )

    def actions_process_delete_element(
        self, id: str, command: _models.ProcessDeleteElementCommand, **kwargs: Any
    ) -> _models.Process:
        """Delete an element by code.

        Allow to delete a process element by specifying the item definition code.

        Remove all the element values.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to delete an element. Required.
        :type command: ~kuflow.rest.models.ProcessDeleteElementCommand
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.actions_process_delete_element(
            id=id, command=command, **kwargs
        )

    def actions_process_complete(self, id: str, **kwargs: Any) -> _models.Process:
        """Complete a Process.

        Complete a Process. The state of Process is set to 'completed'.

        If you are already in this state, no action is taken.

        :param id: The resource ID. Required.
        :type id: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.actions_process_complete(id=id, **kwargs)

    def actions_process_cancel(self, id: str, **kwargs: Any) -> _models.Process:
        """Cancel a Process.

        Cancel a Process. The Process state is set to 'cancelled'.

        All the active tasks will be marked as cancelled too.

        If you are already in this state, no action is taken.

        :param id: The resource ID. Required.
        :type id: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.actions_process_cancel(id=id, **kwargs)

    def actions_process_save_user_action_value_document(
        self,
        id: str,
        file: _models.Document,
        command: _models.ProcessSaveUserActionValueDocumentCommand,
        **kwargs: Any,
    ) -> Optional[_models.Process]:
        """Upload and save a document in a user action.

        Allow saving a user action document uploading the content.

        :param id: The resource ID. Required.
        :type id: str
        :param file: Document to save. Required.
        :type file: _models.Document
        :keyword command: User action info. Required.
        :type command: _models.ProcessSaveUserActionValueDocumentCommand
        :return: Process or None
        :rtype: ~kuflow.rest.models.Process or None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return (
            self._kuflow_client.process.actions_process_save_user_action_value_document(
                id=id,
                file=file.file_content,
                file_content_type=file.content_type,
                file_name=file.file_mame,
                user_action_value_id=command.user_action_value_id,
                **kwargs,
            )
        )

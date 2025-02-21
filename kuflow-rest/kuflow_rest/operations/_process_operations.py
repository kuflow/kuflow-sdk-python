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
        sort: Optional[Union[str, list[str]]] = None,
        tenant_id: Optional[Union[str, list[str]]] = None,
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
        :keyword tenant_id: Filter processes that exists in one of tenant ids. Default value is None.
        :type tenant_id: Optional[Union[str, List[str]]]
        :return: ProcessPage
        :rtype: ~kuflow.rest.models.ProcessPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if sort is not None and isinstance(sort, str):
            sort = [sort]

        if tenant_id is not None and isinstance(tenant_id, str):
            tenant_id = [tenant_id]

        return self._kuflow_client.process.find_processes(
            size=size, page=page, sort=sort, tenant_id=tenant_id, **kwargs
        )

    def create_process(self, process_create_params: _models.ProcessCreateParams, **kwargs: Any) -> _models.Process:
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

        :param process_create_params: Process to create. Required.
        :type process_create_params: ~kuflow.rest.models.ProcessCreateParams
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.create_process(process_create_params=process_create_params, **kwargs)

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

    def complete_process(self, id: str, **kwargs: Any) -> _models.Process:
        """Complete a Process.

        Complete a Process. The state of Process is set to 'completed'.

        If you are already in this state, no action is taken.

        :param id: The resource ID. Required.
        :type id: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.complete_process(id=id, **kwargs)

    def cancel_process(self, id: str, **kwargs: Any) -> _models.Process:
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
        return self._kuflow_client.process.cancel_process(id=id, **kwargs)

    def change_process_initiator(
        self, id: str, process_change_initiator_params: _models.ProcessChangeInitiatorParams, **kwargs: Any
    ) -> _models.Process:
        """Change process initiator.

        Change the current initiator of a process.

        Allows you to choose a user (by email or principal identifier) or an application (principal
        identifier).
        Only one option will be necessary.

        :param id: The resource ID. Required.
        :type id: str
        :param process_change_initiator_params: Command to change the process initiator. Required.
        :type process_change_initiator_params: ~kuflow.rest.models.ProcessChangeInitiatorParams
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.change_process_initiator(
            id=id, process_change_initiator_params=process_change_initiator_params, **kwargs
        )

    def upload_process_user_action_document(
        self,
        id: str,
        file: _models.Document,
        user_action_value_id: str,
        **kwargs: Any,
    ) -> Optional[_models.Process]:
        """Upload and save a document in a user action.

        Allow saving a user action document uploading the content.

        user_action_value_id:

        :param id: The resource ID. Required.
        :type id: str
        :param file: Document to save. Required.
        :type file: _models.Document
        :keyword user_action_value_id: User action value id. Required.
        :type user_action_value_id: _models.ProcessUserActionUploadParams
        :return: Process or None
        :rtype: ~kuflow.rest.models.Process or None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.upload_process_user_action_document(
            id=id,
            file=file.file_content,
            file_content_type=file.content_type,
            file_name=file.file_mame,
            user_action_value_id=user_action_value_id,
            **kwargs,
        )

    def update_process_metadata(
        self, id: str, process_metadata_update_params: _models.ProcessMetadataUpdateParams, **kwargs: Any
    ) -> _models.Process:
        """Save process metadata.

        Save process metadata.

        :param id: The resource ID. Required.
        :type id: str
        :param process_metadata_update_params: Params to save the metadata data. Required.
        :type process_metadata_update_params: ~kuflow.rest.models.ProcessSaveElementCommand
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.update_process_metadata(
            id=id, process_metadata_update_params=process_metadata_update_params, **kwargs
        )

    def patch_process_metadata(
        self, id: str, json_patch: list[_models.JsonPatchOperation], **kwargs: Any
    ) -> _models.Process:
        """Patch JSON data.

        Allow to patch a JSON data validating that the data follow the related schema. If the data is
        invalid, then
        the json is marked as invalid.

        :param id: The resource ID. Required.
        :type id: str
        :param json_patch: Params to save the metadata data. Required.
        :type json_patch: List[~kuflow.rest.models.JsonPatchOperation]
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.patch_process_metadata(id=id, json_patch=json_patch, **kwargs)

    def update_process_entity(
        self,
        id: str,
        process_entity_update_params: _models.ProcessEntityUpdateParams,
        **kwargs: Any,
    ) -> _models.Process:
        """Save JSON data.

        Allow to save a JSON validating that the data follow the related schema. If the data is
        invalid, then
        the json form is marked as invalid.

        :param id: The resource ID. Required.
        :type id: str
        :param process_entity_update_params: Params to save the JSON value. Required.
        :type process_entity_update_params: ~kuflow.rest.models.ProcessEntityUpdateParams
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.update_process_entity(
            id=id, process_entity_update_params=process_entity_update_params, **kwargs
        )

    def patch_process_entity(
        self,
        id: str,
        json_patch: list[_models.JsonPatchOperation],
        **kwargs: Any,
    ) -> _models.Process:
        """Save JSON data.

        Allow to save a JSON validating that the data follow the related schema. If the data is
        invalid, then
        the json form is marked as invalid.

        :param id: The resource ID. Required.
        :type id: str
        :param json_patch: Params to save the JSON value. Required.
        :type json_patch: List[~kuflow.rest.models.JsonPatchOperation]
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.patch_process_entity(id=id, json_patch=json_patch, **kwargs)

    def upload_process_document(self, id: str, document: _models.Document, **kwargs: Any) -> _models.DocumentReference:
        """Upload a temporal document into the process that later on must be linked with a process domain
        resource.

        Upload a temporal document into the process that later on must be linked with a process domain
        resource.

        Documents uploaded with this API will be deleted after 24 hours as long as they have not been
        linked to a
        process or process item.

        :param id: The resource ID. Required.
        :type id: str
        :param document: Document to save. Required.
        :type document: ~kuflow.rest.models.Document
        :return: DocumentReference
        :rtype: ~kuflow.rest.models.DocumentReference
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.upload_process_document(
            id=id,
            document=document.file_content,
            file_content_type=document.content_type,
            file_name=document.file_mame,
            **kwargs,
        )

    def download_process_document(self, id: str, *, document_uri: str, **kwargs: Any) -> Iterator[bytes]:
        """Download document.

        Given a process and a documentUri, download a document.

        :param id: The resource ID. Required.
        :type id: str
        :keyword document_uri: Document URI to download. Required.
        :type document_uri: str
        :return: Iterator[bytes]
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.process.download_process_document(id=id, document_uri=document_uri, **kwargs)

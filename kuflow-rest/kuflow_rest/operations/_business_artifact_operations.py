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


class BusinessArtifactOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`business_artifact` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def find_business_artifacts(
        self,
        size: int = 25,
        page: int = 0,
        sort: Optional[Union[str, list[str]]] = None,
        tenant_id: Optional[Union[str, list[str]]] = None,
        business_artifact_definition_id: Optional[Union[str, list[str]]] = None,
        business_artifact_definition_code: Optional[Union[str, list[str]]] = None,
        value: Optional[Union[str, list[str]]] = None,
        **kwargs: Any,
    ) -> _models.BusinessArtifactPage:
        """Find all accessible Business Artifacts.

        List all the Business Artifacts that have been created and the credentials has access.

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
        :keyword tenant_id: Filter by tenantId. Default value is None.
        :type tenant_id: Optional[Union[str, List[str]]]
        :keyword business_artifact_definition_id: Filter by an array of business artifact definition ids.
                                                  Default value is None.
        :type business_artifact_definition_id: Optional[Union[str, List[str]]]
        :keyword business_artifact_definition_code: Filter by an array of business artifact definition codes.
                                                    Default value is None.
        :type business_artifact_definition_code: Optional[Union[str, List[str]]]
        :keyword value: Filter by an array of values. Default value is None.
        :type value: Optional[Union[str, List[str]]]
        :return: BusinessArtifactPage
        :rtype: ~kuflow.rest.models.BusinessArtifactPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if sort is not None and isinstance(sort, str):
            sort = [sort]

        if tenant_id is not None and isinstance(tenant_id, str):
            tenant_id = [tenant_id]

        if business_artifact_definition_id is not None and isinstance(business_artifact_definition_id, str):
            business_artifact_definition_id = [business_artifact_definition_id]

        if business_artifact_definition_code is not None and isinstance(business_artifact_definition_code, str):
            business_artifact_definition_code = [business_artifact_definition_code]

        if value is not None and isinstance(value, str):
            value = [value]

        return self._kuflow_client.business_artifact.find_business_artifacts(
            size=size,
            page=page,
            sort=sort,
            tenant_id=tenant_id,
            business_artifact_definition_id=business_artifact_definition_id,
            business_artifact_definition_code=business_artifact_definition_code,
            value=value,
            **kwargs,
        )

    def create_business_artifact(
        self, business_artifact_create_params: _models.BusinessArtifactCreateParams, **kwargs: Any
    ) -> _models.BusinessArtifact:
        """Create a new Business Artifact.

        Creates a Business Artifact.

        If you want the method to be idempotent, please specify the ``id`` field in the request body.

        :param business_artifact_create_params: Business Artifact to create. Required.
        :type business_artifact_create_params: ~kuflow.rest.models.BusinessArtifactCreateParams
        :return: BusinessArtifact
        :rtype: ~kuflow.rest.models.BusinessArtifact
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.create_business_artifact(
            business_artifact_create_params=business_artifact_create_params, **kwargs
        )

    def retrieve_business_artifact(self, id: str, **kwargs: Any) -> _models.BusinessArtifact:
        """Get a Business Artifact by ID.

        Returns the requested Business Artifact when has access to do it.

        :param id: The resource ID. Required.
        :type id: str
        :return: BusinessArtifact
        :rtype: ~kuflow.rest.models.BusinessArtifact
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.retrieve_business_artifact(id=id, **kwargs)

    def delete_business_artifact(self, id: str, **kwargs: Any) -> None:
        """Delete a Business Artifact by ID.

        Deletes the requested Business Artifact.

        :param id: The resource ID. Required.
        :type id: str
        :return: None
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.delete_business_artifact(id=id, **kwargs)

    def update_business_artifact_data(
        self, id: str, business_artifact_data_update_params: _models.BusinessArtifactDataUpdateParams, **kwargs: Any
    ) -> _models.BusinessArtifact:
        """Save JSON data.

        Allow to save a JSON data validating that the data follow the related schema. If the data is
        invalid, then the json is marked as invalid.

        :param id: The resource ID. Required.
        :type id: str
        :param business_artifact_data_update_params: Params used to update the JSON value. Required.
        :type business_artifact_data_update_params: ~kuflow.rest.models.BusinessArtifactDataUpdateParams
        :return: BusinessArtifact
        :rtype: ~kuflow.rest.models.BusinessArtifact
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.update_business_artifact_data(
            id=id, business_artifact_data_update_params=business_artifact_data_update_params, **kwargs
        )

    def patch_business_artifact_data(
        self, id: str, json_patch: list[_models.JsonPatchOperation], **kwargs: Any
    ) -> _models.BusinessArtifact:
        """Patch JSON data.

        Allow to patch a JSON data validating that the data follow the related schema. If the data is
        invalid, then the json is marked as invalid.

        :param id: The resource ID. Required.
        :type id: str
        :param json_patch: Params to save the JSON value. Required.
        :type json_patch: List[~kuflow.rest.models.JsonPatchOperation]
        :return: BusinessArtifact
        :rtype: ~kuflow.rest.models.BusinessArtifact
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.patch_business_artifact_data(
            id=id, json_patch=json_patch, **kwargs
        )

    def create_business_artifact_action(
        self, id: str, business_artifact_action_create_params: _models.BusinessArtifactActionCreateParams, **kwargs: Any
    ) -> _models.BusinessArtifactAction:
        """Invoke a Business Artifact action.

        Invoke an action on a Business Artifact.

        If you want the method to be idempotent, please specify the ``id`` field in the request body.

        :param id: The resource ID. Required.
        :type id: str
        :param business_artifact_action_create_params: Business Artifact action to invoke. Required.
        :type business_artifact_action_create_params: ~kuflow.rest.models.BusinessArtifactActionCreateParams
        :return: BusinessArtifactAction
        :rtype: ~kuflow.rest.models.BusinessArtifactAction
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.create_business_artifact_action(
            id=id, business_artifact_action_create_params=business_artifact_action_create_params, **kwargs
        )

    def retrieve_business_artifact_action(
        self, id: str, action_id: str, **kwargs: Any
    ) -> _models.BusinessArtifactAction:
        """Get a Business Artifact action by ID.

        Returns a Business Artifact action by its ID.

        :param id: The resource ID. Required.
        :type id: str
        :param action_id: The Business Artifact action ID. Required.
        :type action_id: str
        :return: BusinessArtifactAction
        :rtype: ~kuflow.rest.models.BusinessArtifactAction
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.retrieve_business_artifact_action(
            id=id, action_id=action_id, **kwargs
        )

    def cancel_business_artifact_action(self, id: str, action_id: str, **kwargs: Any) -> _models.BusinessArtifactAction:
        """Cancel a Business Artifact action.

        Cancel a Business Artifact action by its ID.

        :param id: The resource ID. Required.
        :type id: str
        :param action_id: The Business Artifact action ID. Required.
        :type action_id: str
        :return: BusinessArtifactAction
        :rtype: ~kuflow.rest.models.BusinessArtifactAction
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.cancel_business_artifact_action(
            id=id, action_id=action_id, **kwargs
        )

    def prepare_business_artifact_create_artifact(
        self,
        id: str,
        business_artifact_create_artifact_prepare_params: _models.BusinessArtifactCreateArtifactPrepareParams,
        **kwargs: Any,
    ) -> _models.BusinessArtifactCreateArtifactPrepare:
        """Prepare the data for a CREATE_BUSINESS_ARTIFACT action.

        Compute the pre-filled value that a ``CREATE_BUSINESS_ARTIFACT`` action would produce
        for this Business Artifact, without invoking the action or persisting any state.

        :param id: The resource ID. Required.
        :type id: str
        :param business_artifact_create_artifact_prepare_params: Params identifying the
         CREATE_BUSINESS_ARTIFACT action to prepare. Required.
        :type business_artifact_create_artifact_prepare_params:
         ~kuflow.rest.models.BusinessArtifactCreateArtifactPrepareParams
        :return: BusinessArtifactCreateArtifactPrepare
        :rtype: ~kuflow.rest.models.BusinessArtifactCreateArtifactPrepare
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.prepare_business_artifact_create_artifact(
            id=id,
            business_artifact_create_artifact_prepare_params=business_artifact_create_artifact_prepare_params,
            **kwargs,
        )

    def upload_business_artifact_document(
        self, id: str, document: _models.Document, **kwargs: Any
    ) -> _models.DocumentReference:
        """Upload a temporal document into the business artifact that later on must be linked with a
        business artifact domain resource.

        Documents uploaded with this API will be deleted after 2 hours as long as they have not been
        linked to a business artifact.

        :param id: The resource ID. Required.
        :type id: str
        :param document: Document to save. Required.
        :type document: ~kuflow.rest.models.Document
        :return: DocumentReference
        :rtype: ~kuflow.rest.models.DocumentReference
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.upload_business_artifact_document(
            id=id,
            file=document.file_content,
            file_content_type=document.content_type,
            file_name=document.file_name,
            **kwargs,
        )

    def download_business_artifact_document(self, id: str, *, document_uri: str, **kwargs: Any) -> Iterator[bytes]:
        """Download document.

        Given a business artifact and a documentUri, download a document.

        :param id: The resource ID. Required.
        :type id: str
        :keyword document_uri: Document URI to download. Required.
        :type document_uri: str
        :return: Iterator[bytes]
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.business_artifact.download_business_artifact_document(
            id=id, document_uri=document_uri, **kwargs
        )

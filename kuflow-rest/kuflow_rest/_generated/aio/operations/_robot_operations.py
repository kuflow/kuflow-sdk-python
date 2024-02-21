# pylint: disable=too-many-lines,too-many-statements
# coding=utf-8
# --------------------------------------------------------------------------
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
# --------------------------------------------------------------------------
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
#
# --------------------------------------------------------------------------
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, TypeVar, Union

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.rest import AsyncHttpResponse, HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async

from ... import models as _models
from ...operations._robot_operations import (
    build_actions_robot_download_asset_request,
    build_actions_robot_download_source_code_request,
    build_find_robots_request,
    build_retrieve_robot_request,
)

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class RobotOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.aio.KuFlowRestClient`'s
        :attr:`robot` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace_async
    async def find_robots(
        self,
        *,
        size: int = 25,
        page: int = 0,
        sort: Optional[List[str]] = None,
        tenant_id: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> _models.RobotPage:
        """Find all accessible Robots.

        List all the Robots that have been created and the credentials has access.

        Available sort query values: createdAt, lastModifiedAt.

        :keyword size: The number of records returned within a single API call. Default value is 25.
        :paramtype size: int
        :keyword page: The page number of the current page in the returned records, 0 is the first
         page. Default value is 0.
        :paramtype page: int
        :keyword sort: Sorting criteria in the format: property{,asc|desc}. Example: createdAt,desc

         Default sort order is ascending. Multiple sort criteria are supported.

         Please refer to the method description for supported properties. Default value is None.
        :paramtype sort: list[str]
        :keyword tenant_id: Filter by tenantId. Default value is None.
        :paramtype tenant_id: list[str]
        :return: RobotPage
        :rtype: ~kuflow.rest.models.RobotPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = kwargs.pop("params", {}) or {}

        cls: ClsType[_models.RobotPage] = kwargs.pop("cls", None)

        _request = build_find_robots_request(
            size=size,
            page=page,
            sort=sort,
            tenant_id=tenant_id,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                await response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("RobotPage", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def retrieve_robot(self, id: str, **kwargs: Any) -> _models.Robot:
        """Get a Robot by ID.

        Returns the requested Robot when has access to do it.

        :param id: The resource ID. Required.
        :type id: str
        :return: Robot
        :rtype: ~kuflow.rest.models.Robot
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = kwargs.pop("params", {}) or {}

        cls: ClsType[_models.Robot] = kwargs.pop("cls", None)

        _request = build_retrieve_robot_request(
            id=id,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                await response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("Robot", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def actions_robot_download_source_code(self, id: str, **kwargs: Any) -> AsyncIterator[bytes]:
        """Download robot code.

        Given a robot, download the source code.

        :param id: The resource ID. Required.
        :type id: str
        :return: Async iterator of the response bytes
        :rtype: AsyncIterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = kwargs.pop("params", {}) or {}

        cls: ClsType[AsyncIterator[bytes]] = kwargs.pop("cls", None)

        _request = build_actions_robot_download_source_code_request(
            id=id,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = True
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                await response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = response.iter_bytes()

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def actions_robot_download_asset(
        self,
        id: str,
        *,
        type: Union[str, _models.RobotAssetType],
        version: str,
        platform: Union[str, _models.RobotAssetPlatform],
        architecture: Union[str, _models.RobotAssetArchitecture],
        **kwargs: Any,
    ) -> AsyncIterator[bytes]:
        """Download robot asset.

        Given a robot, download the requested asset.

        :param id: The resource ID. Required.
        :type id: str
        :keyword type: The asset type. Known values are: "PYTHON", "PYTHON_PIP", and "NODEJS".
         Required.
        :paramtype type: str or ~kuflow.rest.models.RobotAssetType
        :keyword version: The asset version. Required.
        :paramtype version: str
        :keyword platform: The asset platform. Known values are: "WINDOWS", "MAC_OS", and "LINUX".
         Required.
        :paramtype platform: str or ~kuflow.rest.models.RobotAssetPlatform
        :keyword architecture: The asset platform architecture. Known values are: "X86_32" and
         "X86_64". Required.
        :paramtype architecture: str or ~kuflow.rest.models.RobotAssetArchitecture
        :return: Async iterator of the response bytes
        :rtype: AsyncIterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = kwargs.pop("params", {}) or {}

        cls: ClsType[AsyncIterator[bytes]] = kwargs.pop("cls", None)

        _request = build_actions_robot_download_asset_request(
            id=id,
            type=type,
            version=version,
            platform=platform,
            architecture=architecture,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = True
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                await response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = response.iter_bytes()

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore
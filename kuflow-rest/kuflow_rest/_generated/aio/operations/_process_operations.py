# pylint: disable=too-many-lines
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
from typing import Any, Callable, Dict, IO, List, Optional, TypeVar, Union, overload

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict

from ... import models as _models
from ...operations._process_operations import (
    build_actions_process_cancel_request,
    build_actions_process_change_initiator_request,
    build_actions_process_complete_request,
    build_actions_process_delete_element_request,
    build_actions_process_save_element_request,
    build_actions_process_save_user_action_value_document_request,
    build_create_process_request,
    build_find_processes_request,
    build_retrieve_process_request,
)

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class ProcessOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.aio.KuFlowRestClient`'s
        :attr:`process` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace_async
    async def find_processes(
        self, *, size: int = 25, page: int = 0, sort: Optional[List[str]] = None, **kwargs: Any
    ) -> _models.ProcessPage:
        """Find all accessible Processes.

        List all the Processes that have been created and the credentials has access.

        Available sort query values: id, createdAt, lastModifiedAt.

        :keyword size: The number of records returned within a single API call. Default value is 25.
        :paramtype size: int
        :keyword page: The page number of the current page in the returned records, 0 is the first
         page. Default value is 0.
        :paramtype page: int
        :keyword sort: Sorting criteria in the format: property{,asc|desc}. Example: createdAt,desc

         Default sort order is ascending. Multiple sort criteria are supported.

         Please refer to the method description for supported properties. Default value is None.
        :paramtype sort: list[str]
        :return: ProcessPage
        :rtype: ~kuflow.rest.models.ProcessPage
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

        cls: ClsType[_models.ProcessPage] = kwargs.pop("cls", None)

        request = build_find_processes_request(
            size=size,
            page=page,
            sort=sort,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("ProcessPage", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    @overload
    async def create_process(
        self, process: _models.Process, *, content_type: str = "application/json", **kwargs: Any
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
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def create_process(
        self, process: IO, *, content_type: str = "application/json", **kwargs: Any
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
        :type process: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def create_process(self, process: Union[_models.Process, IO], **kwargs: Any) -> _models.Process:
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

        :param process: Process to create. Is either a model type or a IO type. Required.
        :type process: ~kuflow.rest.models.Process or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Process] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(process, (IO, bytes)):
            _content = process
        else:
            _json = self._serialize.body(process, "Process")

        request = build_create_process_request(
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        if response.status_code == 200:
            deserialized = self._deserialize("Process", pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize("Process", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def retrieve_process(self, id: str, **kwargs: Any) -> _models.Process:
        """Get a Process by ID.

        Returns the requested Process when has access to do it.

        :param id: The resource ID. Required.
        :type id: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
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

        cls: ClsType[_models.Process] = kwargs.pop("cls", None)

        request = build_retrieve_process_request(
            id=id,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("Process", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    @overload
    async def actions_process_change_initiator(
        self,
        id: str,
        command: _models.ProcessChangeInitiatorCommand,
        *,
        content_type: str = "application/json",
        **kwargs: Any,
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
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def actions_process_change_initiator(
        self, id: str, command: IO, *, content_type: str = "application/json", **kwargs: Any
    ) -> _models.Process:
        """Change process initiator.

        Change the current initiator of a process.

        Allows you to choose a user (by email or principal identifier) or an application (principal
        identifier).
        Only one option will be necessary.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to change the process initiator. Required.
        :type command: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def actions_process_change_initiator(
        self, id: str, command: Union[_models.ProcessChangeInitiatorCommand, IO], **kwargs: Any
    ) -> _models.Process:
        """Change process initiator.

        Change the current initiator of a process.

        Allows you to choose a user (by email or principal identifier) or an application (principal
        identifier).
        Only one option will be necessary.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to change the process initiator. Is either a model type or a IO type.
         Required.
        :type command: ~kuflow.rest.models.ProcessChangeInitiatorCommand or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Process] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(command, (IO, bytes)):
            _content = command
        else:
            _json = self._serialize.body(command, "ProcessChangeInitiatorCommand")

        request = build_actions_process_change_initiator_request(
            id=id,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("Process", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    @overload
    async def actions_process_save_element(
        self,
        id: str,
        command: _models.ProcessSaveElementCommand,
        *,
        content_type: str = "application/json",
        **kwargs: Any,
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
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def actions_process_save_element(
        self, id: str, command: IO, *, content_type: str = "application/json", **kwargs: Any
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
        :type command: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def actions_process_save_element(
        self, id: str, command: Union[_models.ProcessSaveElementCommand, IO], **kwargs: Any
    ) -> _models.Process:
        """Save a process element, aka: metadata.

        Allow to save an element.

        If values already exist for the provided element code, it replaces them with the new ones,
        otherwise it creates them. The values of the previous elements that no longer exist will be
        deleted.

        If the process is already finished the invocations fails with an error.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to save an element. Is either a model type or a IO type. Required.
        :type command: ~kuflow.rest.models.ProcessSaveElementCommand or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Process] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(command, (IO, bytes)):
            _content = command
        else:
            _json = self._serialize.body(command, "ProcessSaveElementCommand")

        request = build_actions_process_save_element_request(
            id=id,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("Process", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    @overload
    async def actions_process_delete_element(
        self,
        id: str,
        command: _models.ProcessDeleteElementCommand,
        *,
        content_type: str = "application/json",
        **kwargs: Any,
    ) -> _models.Process:
        """Delete an element by code.

        Allow to delete a process element by specifying the item definition code.

        Remove all the element values.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to delete an element. Required.
        :type command: ~kuflow.rest.models.ProcessDeleteElementCommand
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def actions_process_delete_element(
        self, id: str, command: IO, *, content_type: str = "application/json", **kwargs: Any
    ) -> _models.Process:
        """Delete an element by code.

        Allow to delete a process element by specifying the item definition code.

        Remove all the element values.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to delete an element. Required.
        :type command: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def actions_process_delete_element(
        self, id: str, command: Union[_models.ProcessDeleteElementCommand, IO], **kwargs: Any
    ) -> _models.Process:
        """Delete an element by code.

        Allow to delete a process element by specifying the item definition code.

        Remove all the element values.

        :param id: The resource ID. Required.
        :type id: str
        :param command: Command to delete an element. Is either a model type or a IO type. Required.
        :type command: ~kuflow.rest.models.ProcessDeleteElementCommand or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Process] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(command, (IO, bytes)):
            _content = command
        else:
            _json = self._serialize.body(command, "ProcessDeleteElementCommand")

        request = build_actions_process_delete_element_request(
            id=id,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("Process", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    @distributed_trace_async
    async def actions_process_complete(self, id: str, **kwargs: Any) -> _models.Process:
        """Complete a Process.

        Complete a Process. The state of Process is set to 'completed'.

        If you are already in this state, no action is taken.

        :param id: The resource ID. Required.
        :type id: str
        :return: Process
        :rtype: ~kuflow.rest.models.Process
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

        cls: ClsType[_models.Process] = kwargs.pop("cls", None)

        request = build_actions_process_complete_request(
            id=id,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("Process", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    @distributed_trace_async
    async def actions_process_cancel(self, id: str, **kwargs: Any) -> _models.Process:
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
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = kwargs.pop("params", {}) or {}

        cls: ClsType[_models.Process] = kwargs.pop("cls", None)

        request = build_actions_process_cancel_request(
            id=id,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize("Process", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    @distributed_trace_async
    async def actions_process_save_user_action_value_document(
        self, id: str, file: IO, *, file_content_type: str, file_name: str, user_action_value_id: str, **kwargs: Any
    ) -> Optional[_models.Process]:
        """Upload and save a document in a user action.

        Allow saving a user action document uploading the content.

        :param id: The resource ID. Required.
        :type id: str
        :param file: Document to save. Required.
        :type file: IO
        :keyword file_content_type: Document content type. Required.
        :paramtype file_content_type: str
        :keyword file_name: Document name. Required.
        :paramtype file_name: str
        :keyword user_action_value_id: User action value ID related to de document. Required.
        :paramtype user_action_value_id: str
        :return: Process or None
        :rtype: ~kuflow.rest.models.Process or None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        content_type: str = kwargs.pop("content_type", _headers.pop("Content-Type", "application/octet-stream"))
        cls: ClsType[Optional[_models.Process]] = kwargs.pop("cls", None)

        _content = file

        request = build_actions_process_save_user_action_value_document_request(
            id=id,
            file_content_type=file_content_type,
            file_name=file_name,
            user_action_value_id=user_action_value_id,
            content_type=content_type,
            content=_content,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 304]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.DefaultError, pipeline_response)
            raise HttpResponseError(response=response, model=error)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("Process", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
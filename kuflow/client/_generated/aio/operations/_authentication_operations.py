# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.9.3, generator: @autorest/python@6.2.9)
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, Callable, Dict, IO, Optional, TypeVar, Union, overload

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
from ...operations._authentication_operations import build_create_authentication_request

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class AuthenticationOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.client.aio.KuFlowClient`'s
        :attr:`authentication` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @overload
    async def create_authentication(
        self, authentication: _models.Authentication, *, content_type: str = "application/json", **kwargs: Any
    ) -> _models.Authentication:
        """Create an authentication for the current principal.

        Create an authentication for the current principal.

        :param authentication: Authentication to be created. Required.
        :type authentication: ~kuflow.client.models.Authentication
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Authentication
        :rtype: ~kuflow.client.models.Authentication
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def create_authentication(
        self, authentication: IO, *, content_type: str = "application/json", **kwargs: Any
    ) -> _models.Authentication:
        """Create an authentication for the current principal.

        Create an authentication for the current principal.

        :param authentication: Authentication to be created. Required.
        :type authentication: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: Authentication
        :rtype: ~kuflow.client.models.Authentication
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def create_authentication(
        self, authentication: Union[_models.Authentication, IO], **kwargs: Any
    ) -> _models.Authentication:
        """Create an authentication for the current principal.

        Create an authentication for the current principal.

        :param authentication: Authentication to be created. Is either a model type or a IO type.
         Required.
        :type authentication: ~kuflow.client.models.Authentication or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :return: Authentication
        :rtype: ~kuflow.client.models.Authentication
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
        cls: ClsType[_models.Authentication] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(authentication, (IO, bytes)):
            _content = authentication
        else:
            _json = self._serialize.body(authentication, "Authentication")

        request = build_create_authentication_request(
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

        deserialized = self._deserialize("Authentication", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

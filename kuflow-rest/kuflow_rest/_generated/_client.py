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

from copy import deepcopy
from typing import Any, TYPE_CHECKING
from typing_extensions import Self

from azure.core import PipelineClient
from azure.core.pipeline import policies
from azure.core.rest import HttpRequest, HttpResponse

from . import models as _models
from ._configuration import KuFlowRestClientConfiguration
from ._serialization import Deserializer, Serializer
from .operations import (
    AuthenticationOperations,
    PrincipalOperations,
    ProcessItemOperations,
    ProcessOperations,
    RobotOperations,
    TenantOperations,
    TenantUserOperations,
    WorkerOperations,
)

if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential


class KuFlowRestClient:  # pylint: disable=client-accepts-api-version-keyword,too-many-instance-attributes
    """Introduction
    ============

    This document contains the KuFlow REST API reference. This API is a fundamental part in the
    integration of external
    systems with KuFlow and is used, among others, by the different implementations of the Workers
    that connect to our
    network.

    API Versioning
    ==============

    A versioning strategy allows our clients to continue using the existing REST API and migrate
    their applications to
    the newer API when they are ready.

    The scheme followed is a simplification of *Semver* where only MAJOR versions are
    differentiated from MINOR or PATCH
    versions, i.e. a version number of only two levels is used. With this approach, you only have
    to migrate your
    applications if you want to upgrade to a MAJOR version of the KuFlow API. In case you want to
    upgrade to a MINOR
    version, you can do so without any incompatibility issues.

    The versioning of the api is done through the URI Path, that is, the version number is included
    in the URI Path. The
    URL structure would be as follows:

    .. code-block:: bash

       https://{endpoint}/v{VERSION}/{api-path}

    Idempotency
    ===========

    The API is designed to support idempotency in order to achieve a correct resilience in the
    implementation of its
    clients. The way to achieve this is very simple, in the methods that create resources, you
    simply have to specify a
    UUID in the input data and the API will respond by creating or returning the resource if it
    previously existed. With
    this mechanism, your systems can implement retry logic without worrying about performing data
    tradeoffs.

    OpenAPI Specification
    =====================

    This API is documented in OpenAPI format. This file allows you to create REST clients with the
    technology of your
    choice automatically.

    :ivar authentication: AuthenticationOperations operations
    :vartype authentication: kuflow.rest.operations.AuthenticationOperations
    :ivar principal: PrincipalOperations operations
    :vartype principal: kuflow.rest.operations.PrincipalOperations
    :ivar tenant: TenantOperations operations
    :vartype tenant: kuflow.rest.operations.TenantOperations
    :ivar tenant_user: TenantUserOperations operations
    :vartype tenant_user: kuflow.rest.operations.TenantUserOperations
    :ivar process: ProcessOperations operations
    :vartype process: kuflow.rest.operations.ProcessOperations
    :ivar process_item: ProcessItemOperations operations
    :vartype process_item: kuflow.rest.operations.ProcessItemOperations
    :ivar worker: WorkerOperations operations
    :vartype worker: kuflow.rest.operations.WorkerOperations
    :ivar robot: RobotOperations operations
    :vartype robot: kuflow.rest.operations.RobotOperations
    :param credential: Credential needed for the client to connect to Azure. Required.
    :type credential: ~azure.core.credentials.TokenCredential
    :keyword endpoint: Service URL. Default value is "https://api.kuflow.com/v2024-06-14".
    :paramtype endpoint: str
    """

    def __init__(
        self, credential: "TokenCredential", *, endpoint: str = "https://api.kuflow.com/v2024-06-14", **kwargs: Any
    ) -> None:
        self._config = KuFlowRestClientConfiguration(credential=credential, **kwargs)
        _policies = kwargs.pop("policies", None)
        if _policies is None:
            _policies = [
                policies.RequestIdPolicy(**kwargs),
                self._config.headers_policy,
                self._config.user_agent_policy,
                self._config.proxy_policy,
                policies.ContentDecodePolicy(**kwargs),
                self._config.redirect_policy,
                self._config.retry_policy,
                self._config.authentication_policy,
                self._config.custom_hook_policy,
                self._config.logging_policy,
                policies.DistributedTracingPolicy(**kwargs),
                policies.SensitiveHeaderCleanupPolicy(**kwargs) if self._config.redirect_policy else None,
                self._config.http_logging_policy,
            ]
        self._client: PipelineClient = PipelineClient(base_url=endpoint, policies=_policies, **kwargs)

        client_models = {k: v for k, v in _models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)
        self._serialize.client_side_validation = False
        self.authentication = AuthenticationOperations(self._client, self._config, self._serialize, self._deserialize)
        self.principal = PrincipalOperations(self._client, self._config, self._serialize, self._deserialize)
        self.tenant = TenantOperations(self._client, self._config, self._serialize, self._deserialize)
        self.tenant_user = TenantUserOperations(self._client, self._config, self._serialize, self._deserialize)
        self.process = ProcessOperations(self._client, self._config, self._serialize, self._deserialize)
        self.process_item = ProcessItemOperations(self._client, self._config, self._serialize, self._deserialize)
        self.worker = WorkerOperations(self._client, self._config, self._serialize, self._deserialize)
        self.robot = RobotOperations(self._client, self._config, self._serialize, self._deserialize)

    def send_request(self, request: HttpRequest, *, stream: bool = False, **kwargs: Any) -> HttpResponse:
        """Runs the network request through the client's chained policies.

        >>> from azure.core.rest import HttpRequest
        >>> request = HttpRequest("GET", "https://www.example.org/")
        <HttpRequest [GET], url: 'https://www.example.org/'>
        >>> response = client.send_request(request)
        <HttpResponse: 200 OK>

        For more information on this code flow, see https://aka.ms/azsdk/dpcodegen/python/send_request

        :param request: The network request you want to make. Required.
        :type request: ~azure.core.rest.HttpRequest
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call. Does not do error handling on your response.
        :rtype: ~azure.core.rest.HttpResponse
        """

        request_copy = deepcopy(request)
        request_copy.url = self._client.format_url(request_copy.url)
        return self._client.send_request(request_copy, stream=stream, **kwargs)  # type: ignore

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        self._client.__enter__()
        return self

    def __exit__(self, *exc_details: Any) -> None:
        self._client.__exit__(*exc_details)

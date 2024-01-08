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


import base64
import platform
import sys
from typing import Any, Optional

from azure.core.credentials import AccessToken
from azure.core.pipeline.policies import SansIOHTTPPolicy

from ._generated import VERSION
from ._generated import KuFlowRestClient as KuFlowRestClientGenerated
from .operations import (
    AuthenticationOperations,
    PrincipalOperations,
    ProcessOperations,
    TaskOperations,
    WorkerOperations,
)


class KuFlowClientTokenCredential:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self.token = base64.b64encode(
            "{}:{}".format(client_id, client_secret).encode("utf-8")
        ).decode("utf-8")

    def get_token(
        self,
        *scopes: str,
        claims: Optional[str] = None,
        tenant_id: Optional[str] = None,
        **kwargs: Any,
    ) -> AccessToken:
        """Request an access token for `scopes`.

        :param scopes: The type of access needed.
        :type scopes: str
        :keyword claims: Additional claims required in the token, such as those returned in a resource provider's
                         claims challenge following an authorization failure.
        :type claims: Optional[str]
        :keyword tenant_id: Optional tenant to include in the token request.
        :type tenant_id: Optional[str]
        :rtype: AccessToken
        :return: An AccessToken instance containing the token string and its expiration time in Unix time.
        """
        return AccessToken(token=self.token, expires_on=sys.maxsize)


class AllowHttpPolicy(SansIOHTTPPolicy):
    """A simple policy that allows http requestes adding "enforce_https" to the request context."""

    def on_request(self, request):
        """Updates with the given request id before sending the request to the next policy.

        :param request: The PipelineRequest object
        :type request: ~azure.core.pipeline.PipelineRequest
        """
        options = {"enforce_https": False}
        request.context.options.update(options)


class KuFlowRestClient:  # pylint: disable=client-accepts-api-version-keyword
    API_VERSION = "v2022-10-08"

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
    :vartype authentication: kuflow.rest.client.operations.AuthenticationOperations
    :ivar principal: PrincipalOperations operations
    :vartype principal: kuflow.rest.client.operations.PrincipalOperations
    :ivar process: ProcessOperations operations
    :vartype process: kuflow.rest.client.operations.ProcessOperations
    :ivar task: TaskOperations operations
    :vartype task: kuflow.rest.client.operations.TaskOperations
    :ivar task: WorkerOperations operations
    :vartype task: kuflow.rest.client.operations.WorkerOperations
    :param client_id: Client id used to connect to KuFlow. Required.
    :paramtype client_id: str
    :param client_secret: Client secret used to connect to KuFlow. Required.
    :paramtype client_secret: str
    :keyword endpoint: Service URL. Default value is "https://api.kuflow.com/v2022-10-08".
    :paramtype endpoint: str
    :keyword allow_insecure_connection: Allow non HTTPS endpoints. Default False.
    :paramtype allow_insecure_connection: bool
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        endpoint: Optional[str] = None,
        allow_insecure_connection: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        if endpoint is None:
            endpoint = "https://api.kuflow.com/v2022-10-08"

        per_call_policies = []
        if allow_insecure_connection:
            per_call_policies.append(AllowHttpPolicy())

        if not endpoint.endswith("/" + KuFlowRestClient.API_VERSION):
            endpoint = endpoint + "/" + KuFlowRestClient.API_VERSION

        self._kuflow_client = KuFlowRestClientGenerated(
            credential=KuFlowClientTokenCredential(
                client_id=client_id, client_secret=client_secret
            ),  # type: ignore
            endpoint=endpoint,
            api_version=kwargs.pop("api_version", VERSION),
            credential_scopes="https://api.kuflow.com/v2022-10-08/.default",
            per_call_policies=per_call_policies,
            base_user_agent="sdk-python-kuflow-rest/{} Python/{} ({})".format(
                VERSION, platform.python_version(), platform.platform()
            ),
        )

        self.authentication = AuthenticationOperations(self._kuflow_client)
        self.principal = PrincipalOperations(self._kuflow_client)
        self.process = ProcessOperations(self._kuflow_client)
        self.task = TaskOperations(self._kuflow_client)
        self.worker = WorkerOperations(self._kuflow_client)

    def __enter__(self):
        self._kuflow_client.__enter__()  # pylint:disable=no-member
        return self

    def __exit__(self, *args):
        self._kuflow_client.__exit__(*args)  # pylint:disable=no-member

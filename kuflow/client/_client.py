# coding=utf-8

import sys
import base64

from typing import Any, Optional
from azure.core.credentials import AccessToken
from azure.core.pipeline.policies import SansIOHTTPPolicy

from ._generated import (
    VERSION,
    KuFlowClient as KuFlowClientGenerated
)

from .operations import (
    AuthenticationOperations,
    PrincipalOperations,
    ProcessOperations,
    TaskOperations
)


class KuFlowClientTokenCredential:

    def __init__(
            self,
            username: str,
            password: str,
    ) -> None:
        self.username = username
        self.password = password

        self.token = base64.b64encode("{}:{}".format(username, password).encode('utf-8')).decode('utf-8')

    def get_token(
            self, *scopes: str, claims: Optional[str] = None, tenant_id: Optional[str] = None, **kwargs: Any
    ) -> AccessToken:
        """Request an access token for `scopes`.

        :param str scopes: The type of access needed.

        :keyword str claims: Additional claims required in the token, such as those returned in a resource
            provider's claims challenge following an authorization failure.
        :keyword str tenant_id: Optional tenant to include in the token request.

        :rtype: AccessToken
        :return: An AccessToken instance containing the token string and its expiration time in Unix time.
        """
        return AccessToken(token=self.token, expires_on=sys.maxsize)


class AllowHttpPolicy(SansIOHTTPPolicy):
    """A simple policy that allows http requestes adding "enforce_https" to the request context.
    """

    def on_request(self, request):
        # type: (PipelineRequest) -> None
        """Updates with the given request id before sending the request to the next policy.

        :param request: The PipelineRequest object
        :type request: ~azure.core.pipeline.PipelineRequest
        """
        options = {"enforce_https": False}
        request.context.options.update(options)


class KuFlowClient:  # pylint: disable=client-accepts-api-version-keyword
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
    :vartype authentication: kuflow.client.operations.AuthenticationOperations
    :ivar principal: PrincipalOperations operations
    :vartype principal: kuflow.client.operations.PrincipalOperations
    :ivar process: ProcessOperations operations
    :vartype process: kuflow.client.operations.ProcessOperations
    :ivar task: TaskOperations operations
    :vartype task: kuflow.client.operations.TaskOperations
    :param username: Username used to connect to KuFlow. Required.
    :paramtype username: str
    :param password: Password used to connect to KuFlow. Required.
    :paramtype password: str
    :keyword endpoint: Service URL. Default value is "https://api.kuflow.com/v2022-10-08".
    :paramtype endpoint: str
    :keyword allow_insecure_connection: Allow non HTTPS endpoints. Default False.
    :paramtype allow_insecure_connection: bool
    """

    def __init__(
            self,
            username: str,
            password: str,
            endpoint: str = "https://api.kuflow.com/v2022-10-08",
            allow_insecure_connection: bool = False,
            **kwargs: Any
    ) -> None:
        per_call_policies = []
        if allow_insecure_connection:
            per_call_policies.append(AllowHttpPolicy())

        self._kuflow_client = KuFlowClientGenerated(
            credential=KuFlowClientTokenCredential(username=username, password=password),  # type: ignore
            endpoint=endpoint,
            api_version=kwargs.pop("api_version", VERSION),
            credential_scopes="https://api.kuflow.com//v2022-10-08/.default",
            per_call_policies=per_call_policies
        )

        self.authentication = AuthenticationOperations(self._kuflow_client)
        self.principal = PrincipalOperations(self._kuflow_client)
        self.process = ProcessOperations(self._kuflow_client)
        self.task = TaskOperations(self._kuflow_client)


    def __enter__(self):
        self._kuflow_client.__enter__()  # pylint:disable=no-member
        return self

    def __exit__(self, *args):
        self._kuflow_client.__exit__(*args)  # pylint:disable=no-member

# coding=utf-8
from typing import Any

from azure.core.tracing.decorator import distributed_trace

from .._generated import (
    models as _models,
    KuFlowClient as KuFlowClientGenerated
)


class AuthenticationOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.client.KuFlowClient`'s
        :attr:`authentication` attribute.
    """

    def __init__(self, kuflow_client: KuFlowClientGenerated):
        self.kuflow_client = kuflow_client

    @distributed_trace
    def create_authentication(
        self, authentication: _models.Authentication, **kwargs: Any
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

        return self.kuflow_client.authentication.create_authentication(authentication=authentication, **kwargs)

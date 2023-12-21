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

from typing import Any, TYPE_CHECKING

from azure.core.configuration import Configuration
from azure.core.pipeline import policies

from .._version import VERSION

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core.credentials_async import AsyncTokenCredential


class KuFlowRestClientConfiguration(Configuration):  # pylint: disable=too-many-instance-attributes,name-too-long
    """Configuration for KuFlowRestClient.

    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param credential: Credential needed for the client to connect to Azure. Required.
    :type credential: ~azure.core.credentials_async.AsyncTokenCredential
    """

    def __init__(self, credential: "AsyncTokenCredential", **kwargs: Any) -> None:
        super(KuFlowRestClientConfiguration, self).__init__(**kwargs)
        if credential is None:
            raise ValueError("Parameter 'credential' must not be None.")

        self.credential = credential
        self.credential_scopes = kwargs.pop("credential_scopes", [])
        kwargs.setdefault("sdk_moniker", "kuflow-rest/{}".format(VERSION))
        self._configure(**kwargs)

    def _configure(self, **kwargs: Any) -> None:
        self.user_agent_policy = kwargs.get(
            "user_agent_policy"
        ) or policies.UserAgentPolicy(**kwargs)
        self.headers_policy = kwargs.get("headers_policy") or policies.HeadersPolicy(
            **kwargs
        )
        self.proxy_policy = kwargs.get("proxy_policy") or policies.ProxyPolicy(**kwargs)
        self.logging_policy = kwargs.get(
            "logging_policy"
        ) or policies.NetworkTraceLoggingPolicy(**kwargs)
        self.http_logging_policy = kwargs.get(
            "http_logging_policy"
        ) or policies.HttpLoggingPolicy(**kwargs)
        self.retry_policy = kwargs.get("retry_policy") or policies.AsyncRetryPolicy(
            **kwargs
        )
        self.custom_hook_policy = kwargs.get(
            "custom_hook_policy"
        ) or policies.CustomHookPolicy(**kwargs)
        self.redirect_policy = kwargs.get(
            "redirect_policy"
        ) or policies.AsyncRedirectPolicy(**kwargs)
        self.authentication_policy = kwargs.get("authentication_policy")
        if not self.credential_scopes and not self.authentication_policy:
            raise ValueError(
                "You must provide either credential_scopes or authentication_policy as kwargs"
            )
        if self.credential and not self.authentication_policy:
            self.authentication_policy = policies.AsyncBearerTokenCredentialPolicy(
                self.credential, *self.credential_scopes, **kwargs
            )

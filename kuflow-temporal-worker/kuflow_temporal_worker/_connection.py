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

import dataclasses
from typing import Optional

import temporalio.activity
import temporalio.common
import temporalio.converter
import temporalio.runtime
import temporalio.workflow
from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker

from kuflow_rest import models
from kuflow_temporal_common import (
    KuFlowModelJSONEncoder,
    KuFlowModelJSONTypeConverter,
)

from ._authentication import KuFlowAuthorizationTokenProvider
from ._connection_config import (
    KuFlowConfig,
    TemporalConfig,
)
from ._encryption import (
    KuFlowEncryptionInterceptor,
    KuFlowEncryptionPayloadCodec,
    KuFlowEncryptionPayloadConverter,
)
from ._worker_information_notifier import KuFlowWorkerInformationNotifier


class KuFlowTemporalConnection:
    """Configure a temporal client and worker with KuFlow requirements."""

    def __init__(self, *, kuflow: KuFlowConfig, temporal: TemporalConfig):
        """Create a KuFlowTemporalConnection."""

        self._kuflow = kuflow
        self._temporal = temporal
        self._kuflow_authorization_token_provider: Optional[KuFlowAuthorizationTokenProvider] = None
        self._kuFlow_worker_information_notifier: Optional[KuFlowWorkerInformationNotifier] = None
        self._client: Optional[Client] = None
        self._worker: Optional[Worker] = None
        self._workflow_types: set[str] = set()
        self._activity_types: set[str] = set()

    async def connect(self) -> Client:
        """Connect to a Temporal server"""

        if self._client is not None:
            return self._client

        self._apply_default_configurations()

        # Initializing an KuFlow token provider
        self._kuflow_authorization_token_provider = KuFlowAuthorizationTokenProvider(
            temporal_config=self._temporal,
            kuflow_config=self._kuflow,
        )

        self._temporal.client.rpc_metadata = self._kuflow_authorization_token_provider.initialize_rpc_auth_metadata()

        client_config = self._temporal.client.__dict__.copy()
        client_config.pop("target_host", None)
        client_config["data_converter"] = dataclasses.replace(
            temporalio.converter.DataConverter.default,
            payload_converter_class=KuFlowConverterClass,
            payload_codec=KuFlowEncryptionPayloadCodec(
                rest_client=self._kuflow.rest_client,
            ),
        )
        client_config["interceptors"] = [KuFlowEncryptionInterceptor()]

        target_host = self._temporal.client.target_host or "engine.kuflow.com:443"

        self._client = await Client.connect(target_host, **client_config)

        self._kuflow_authorization_token_provider.start_auto_refresh(self._client)

        return self._client

    async def create_worker(self) -> Worker:
        """Create a new Worker. This method initiates a connection to the server."""

        if self._worker is not None:
            return self._worker

        if self._temporal.worker is None:
            raise TypeError("Worker configurations are required")

        client = await self.connect()

        worker_config = self._temporal.worker.__dict__.copy()
        worker_config["interceptors"] = []

        self._worker = Worker(client, **worker_config)

        return self._worker

    async def run_worker(self):
        """Start the temporal worker configured."""

        worker = await self.create_worker()

        self._workflow_types.clear()
        self._activity_types.clear()

        for workflow in self._temporal.worker.workflows:
            defn = temporalio.workflow._Definition.must_from_class(workflow)
            self._workflow_types.add(defn.name)

        for activity in self._temporal.worker.activities:
            if isinstance(activity, str):
                self._activity_types.add(activity)
            elif callable(activity):
                defn = temporalio.activity._Definition.must_from_callable(activity)
                self._activity_types.add(defn.name)

        self._kuFlow_worker_information_notifier = KuFlowWorkerInformationNotifier(
            kuflow_client=self._kuflow.rest_client,
            kuflow_config=self._kuflow,
            temporal_config=self._temporal,
            temporal_worker=worker,
            temporal_client=self._client,
            temporal_workflow_types=self._workflow_types,
            temporal_activity_types=self._activity_types,
            backoff=self._kuflow.worker_information_notifier_backoff,
        )
        await self._kuFlow_worker_information_notifier.start()

        await worker.run()

    def _apply_default_configurations(self):
        authentication = models.Authentication(
            type=models.AuthenticationType.ENGINE_CERTIFICATE,
            tenant_id=self._kuflow.tenant_id,
        )
        authentication = self._kuflow.rest_client.authentication.create_authentication(authentication)

        if self._temporal.client.tls is False:
            self._temporal.client.tls = TLSConfig(
                server_root_ca_cert=authentication.engine_certificate.tls.server_root_ca_certificate.encode("utf-8"),
                client_cert=authentication.engine_certificate.tls.client_certificate.encode("utf-8"),
                client_private_key=authentication.engine_certificate.tls.client_private_key.encode("utf-8"),
            )

        if self._temporal.client.namespace is None:
            self._temporal.client.namespace = authentication.engine_certificate.namespace

        self._temporal.client.namespace = self._temporal.client.namespace or "default"


class KuFlowConverterClass(temporalio.converter.CompositePayloadConverter):
    def __init__(self) -> None:
        super().__init__(
            temporalio.converter.BinaryNullPayloadConverter(),
            temporalio.converter.BinaryPlainPayloadConverter(),
            temporalio.converter.JSONProtoPayloadConverter(),
            temporalio.converter.BinaryProtoPayloadConverter(),
            KuFlowEncryptionPayloadConverter(
                delegate=temporalio.converter.JSONPlainPayloadConverter(
                    encoder=KuFlowModelJSONEncoder, custom_type_converters=[KuFlowModelJSONTypeConverter()]
                )
            ),
        )

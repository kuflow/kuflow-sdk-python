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

import concurrent.futures
import dataclasses
from dataclasses import dataclass
from datetime import timedelta
from typing import Awaitable, Callable, Dict, List, Mapping, Optional, Sequence, Set, Type, Union

import temporalio.activity
import temporalio.common
import temporalio.converter
import temporalio.runtime
import temporalio.workflow
from temporalio.client import Client, Interceptor, RetryConfig, TLSConfig
from temporalio.worker import SharedStateManager, UnsandboxedWorkflowRunner, Worker, WorkflowRunner
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from kuflow_rest import KuFlowRestClient, models
from kuflow_temporal_common.authentication import (
    KuFlowAuthorizationTokenProvider,
    KuFlowAuthorizationTokenProviderBackoff,
)
from kuflow_temporal_common.converter import CompositeEncodingPayloadConverter
from kuflow_temporal_common.worker_information_notifier import (
    KuFlowWorkerInformationNotifier,
    KuFlowWorkerInformationNotifierBackoff,
)


@dataclass
class KuFlowConfig:
    """KuFlow configuration."""

    rest_client: KuFlowRestClient
    """Rest client used."""

    authorization_token_provider_backoff: Optional[KuFlowAuthorizationTokenProviderBackoff] = None
    """Authorization backoff configuration"""

    worker_information_notifier_backoff: Optional[KuFlowWorkerInformationNotifierBackoff] = None
    """Worker notifier backoff configuration"""


@dataclass
class TemporalClientConfig:
    """Temporal client configuration options."""

    target_host: Optional[str] = None
    """``host:port`` for the Temporal server. For local development, this is often "localhost:7233"."""

    namespace: Optional[str] = None
    """Namespace to use for client calls, this is often "default"."""

    data_converter: temporalio.converter.DataConverter = temporalio.converter.DataConverter.default
    """Data converter to use for all data conversions to/from payloads."""

    interceptors: Optional[Sequence[Interceptor]] = None
    """Set of interceptors that are chained together to allow intercepting of client calls. The earlier interceptors
    wrap the later ones.

    Any interceptors that also implement :py:class:`temporalio.worker.Interceptor` will be used as worker interceptors
    too so they should not be given when creating a worker."""

    default_workflow_query_reject_condition: Optional[temporalio.common.QueryRejectCondition] = None
    """The default rejection condition for workflow queries if not set during query. See :py:meth:`WorkflowHandle.query`
    for details on the rejection condition."""

    tls: Union[bool, TLSConfig] = False
    """If false, the default, do not use TLS. If true, use system default TLS configuration. If TLS configuration
    present, that TLS configuration will be used."""

    retry_config: Optional[RetryConfig] = None
    """Retry configuration for direct service calls (when opted in) or all high-level calls made by this client (which
    all opt-in to retries by default). If unset, a default retry configuration is used."""

    rpc_metadata: Optional[Mapping[str, str]] = None
    """Headers to use for all calls to the server. Keys here can be overriden by per-call RPC metadata keys."""

    identity: Optional[str] = None
    """Identity for this client. If unset, a default is created based on the version of the SDK."""

    lazy: bool = False
    """If true, the client will not connect until the first call is attempted or a worker is created with it. Lazy
    clients cannot be used for workers."""

    runtime: Optional[temporalio.runtime.Runtime] = None
    """The runtime for this client, or the default if unset."""


@dataclass
class TemporalWorkerConfig:
    """Temporal worker configuration options."""

    task_queue: str
    """Required task queue for this worker."""

    activities: Optional[Sequence[Callable]] = None
    """Set of activity callables decorated with :py:func:`@activity.defn<temporalio.activity.defn>`. Activities may be
    async functions or non-async functions. """

    workflows: Optional[Sequence[Type]] = None
    """Set of workflow classes decorated with :py:func:`@workflow.defn<temporalio.workflow.defn>`."""

    activity_executor: Optional[concurrent.futures.Executor] = None
    """Concurrent executor to use for non-async activities. This is required if any activities are non-async. If this is
    a :py:class:`concurrent.futures.ProcessPoolExecutor`, all non-async activities must be picklable. Note, a broken
    executor failure from this executor will cause the worker to fail and shutdown."""

    workflow_task_executor: Optional[concurrent.futures.ThreadPoolExecutor] = None
    """Thread pool executor for workflow tasks. If this is not present, a new
    :py:class:`concurrent.futures.ThreadPoolExecutor` will be created with ``max_workers`` set to
    ``max(os.cpu_count(), 4)``. The default one will be properly shutdown, but if one is provided, the caller is
    responsible for shutting it down after the worker is shut down."""

    workflow_runner: WorkflowRunner = SandboxedWorkflowRunner()
    """Runner for workflows."""

    unsandboxed_workflow_runner: WorkflowRunner = UnsandboxedWorkflowRunner()
    """Runner for workflows that opt-out of sandboxing."""

    interceptors: Optional[Sequence[Interceptor]] = None
    """Collection of interceptors for this worker. Any interceptors already on the client that also implement
    :py:class:`Interceptor` are prepended to this list and should not be explicitly given here."""

    build_id: Optional[str] = None
    """Unique identifier for the current runtime. This is best set as a hash of all code and should change only when
    code does. If unset, a best-effort identifier is generated."""

    identity: Optional[str] = None
    """Identity for this worker client. If unset, the client identity is used."""

    max_cached_workflows: Optional[int] = None
    """If nonzero, workflows will be cached and sticky task queues will be used."""

    max_concurrent_workflow_tasks: Optional[int] = None
    """Maximum allowed number of workflow tasks that will ever be given to this worker at one time."""

    max_concurrent_activities: Optional[int] = None
    """ Maximum number of activity tasks that will ever be given to this worker concurrently."""

    max_concurrent_local_activities: Optional[int] = None
    """Maximum number of local activity tasks that will ever be given to this worker concurrently."""

    max_concurrent_workflow_task_polls: Optional[int] = None
    """Maximum number of concurrent poll workflow task requests we will perform at a time on this worker's task
    queue."""

    nonsticky_to_sticky_poll_ratio: Optional[float] = None
    """max_concurrent_workflow_task_polls * this number = the number of max pollers that will be allowed for the
    nonsticky queue when sticky tasks are enabled. If both defaults are used, the sticky queue will allow 4 max pollers
    while the nonsticky queue will allow one. The minimum for either poller is 1, so if
    ``max_concurrent_workflow_task_polls`` is 1 and sticky queues are enabled, there will be 2 concurrent polls."""

    max_concurrent_activity_task_polls: Optional[int] = None
    """Maximum number of concurrent poll activity task requests we will perform at a time on this worker's task queue.
    """

    no_remote_activities: Optional[bool] = None
    """If true, this worker will only handle workflow tasks and local activities, it will not poll for activity tasks.
    """

    sticky_queue_schedule_to_start_timeout: Optional[timedelta] = None
    """How long a workflow task is allowed to sit on the sticky queue before it is timed out and moved to the non-sticky
     queue where it may be picked up by any worker."""

    max_heartbeat_throttle_interval: Optional[timedelta] = None
    """Longest interval for throttling activity heartbeats."""

    default_heartbeat_throttle_interval: Optional[timedelta] = None
    """Default interval for throttling activity heartbeats in case per-activity heartbeat timeout is unset. Otherwise,
    it's the per-activity heartbeat timeout * 0.8."""

    max_activities_per_second: Optional[float] = None
    """Limits the number of activities per second that this worker will process. The worker will not poll for new
    activities if by doing so it might receive and execute an activity which would cause it to exceed this limit."""

    max_task_queue_activities_per_second: Optional[float] = None
    """Sets the maximum number of activities per second the task queue will dispatch, controlled server-side. Note that
    this only takes effect upon an activity poll request. If multiple workers on the same queue have different values
    set, they will thrash with the last poller winning."""

    graceful_shutdown_timeout: Optional[timedelta] = None
    """Amount of time after shutdown is called that activities are given to complete before their tasks are cancelled.
    """

    shared_state_manager: Optional[SharedStateManager] = None
    """Used for obtaining cross-process friendly synchronization primitives. This is required for non-async activities
    where the activity_executor is not a :py:class:`concurrent.futures.ThreadPoolExecutor`. Reuse of these across
    workers is encouraged."""

    debug_mode: Optional[bool] = None
    """If true, will disable deadlock detection and may disable sandboxing in order to make using a debugger easier. If
    false but the environment variable ``TEMPORAL_DEBUG`` is truthy, this will be set to true."""

    disable_eager_activity_execution: Optional[bool] = None
    """If true, will disable eager activity execution. Eager activity execution is an optimization on some servers that
    sends activities back to the same worker as the calling workflow if they can run there. This setting is experimental
     and may be removed in a future release."""

    on_fatal_error: Optional[Callable[[BaseException], Awaitable[None]]] = None
    """An async function that can handle a failure before the worker shutdown commences. This cannot stop the shutdown
    and any exception raised is logged and ignored."""


@dataclass
class TemporalConfig:
    """Temporal configuration options."""

    client: TemporalClientConfig

    worker: Optional[TemporalWorkerConfig] = None


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
        self._workflow_types: Set[str] = set()
        self._activity_types: Set[str] = set()

    async def connect(self) -> Client:
        """Connect to a Temporal server"""

        if self._client is not None:
            return self._client

        self._apply_default_configurations()

        # Initializing an KuFlow token provider
        self._kuflow_authorization_token_provider = KuFlowAuthorizationTokenProvider(
            kuflow_client=self._kuflow.rest_client,
            backoff=self._kuflow.authorization_token_provider_backoff,
        )

        self._temporal.client.rpc_metadata = self._kuflow_authorization_token_provider.initialize_rpc_auth_metadata()

        self._register_encoding_payload_converter()

        client_config = clean_dict(self._temporal.client.__dict__.copy())
        client_config.pop("target_host", None)

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

        worker_config = clean_dict(self._temporal.worker.__dict__.copy())

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
            temporal_worker=worker,
            temporal_client=self._client,
            temporal_workflow_types=self._workflow_types,
            temporal_activity_types=self._activity_types,
            backoff=self._kuflow.worker_information_notifier_backoff,
        )
        await self._kuFlow_worker_information_notifier.start()

        await worker.run()

    def _register_encoding_payload_converter(self):
        registered_converter_classes = self._get_registered_encoding_payload_converter_classes()
        if len(registered_converter_classes) <= 0:
            return

        converters = list(temporalio.converter.DefaultPayloadConverter.default_encoding_payload_converters)

        converters_by_encoding: Dict[str, List[temporalio.converter.EncodingPayloadConverter]] = {}

        for converter_class in registered_converter_classes:
            converter = converter_class()

            converters_encoding = converters_by_encoding.get(converter.encoding, None)
            if converters_encoding is None:
                converters_encoding = [it for it in converters if it.encoding == converter.encoding]

            converters_encoding.insert(0, converter)
            converters_by_encoding[converter.encoding] = converters_encoding

        for encoding in converters_by_encoding:
            composite_converter = CompositeEncodingPayloadConverter(
                encoding=encoding, converters=converters_by_encoding[encoding]
            )

            converters = [it if it.encoding != encoding else composite_converter for it in converters]

        temporalio.converter.DefaultPayloadConverter.default_encoding_payload_converters = tuple(converters)

        self._temporal.client.data_converter = dataclasses.replace(temporalio.converter.DataConverter.default)

    def _get_registered_encoding_payload_converter_classes(
        self,
    ) -> List[Type[temporalio.converter.EncodingPayloadConverter]]:
        converters = []
        for activity in self._temporal.worker.activities:
            if hasattr(activity, "__kuflow_encoding_payload_converter_class__"):
                converter_class = activity.__kuflow_encoding_payload_converter_class__
                if converter_class not in converters:
                    converters.append(converter_class)

        for workflow in self._temporal.worker.workflows:
            if hasattr(workflow, "__kuflow_encoding_payload_converter_class__"):
                converter_class = workflow.__kuflow_encoding_payload_converter_class__
                if converter_class not in converters:
                    converters.append(converter_class)

        return converters

    def _apply_default_configurations(self):
        authentication = models.Authentication(type=models.AuthenticationType.ENGINE_CERTIFICATE)
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


def clean_dict(value: dict) -> dict:
    return {k: v for k, v in value.items() if v is not None}

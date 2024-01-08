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

import asyncio
import logging
import socket
from typing import Any, Dict, Optional, Set

from azure.core.pipeline import PipelineResponse
from temporalio.client import Client
from temporalio.worker import Worker

from kuflow_rest import KuFlowRestClient, models


logger = logging.getLogger(__name__)


class KuFlowWorkerInformationNotifierBackoff:
    """
    :ivar sleep: Time in seconds to sleep
    :type sleep: int
    :ivar exponential_rate: Increment rate factor
    :type exponential_rate: int
    """

    def __init__(self, sleep: Optional[int] = None, exponential_rate: Optional[int] = None):
        self.sleep = sleep if sleep else 1
        self.exponential_rate = exponential_rate if exponential_rate else 2.5


class KuFlowWorkerInformationNotifier:
    def __init__(
        self,
        kuflow_client: KuFlowRestClient,
        temporal_client: Client,
        temporal_worker: Worker,
        temporal_workflow_types: Optional[Set[str]] = None,
        temporal_activity_types: Optional[Set[str]] = None,
        backoff: Optional[KuFlowWorkerInformationNotifierBackoff] = None,
    ):
        if temporal_workflow_types is None:
            temporal_workflow_types = set()
        if temporal_activity_types is None:
            temporal_activity_types = set()
        if backoff is None:
            backoff = KuFlowWorkerInformationNotifierBackoff()

        self._kuflow_client = kuflow_client
        self._temporal_client = temporal_client
        self._temporal_worker = temporal_worker
        self._temporal_workflow_types: Set[str] = temporal_workflow_types
        self._temporal_activity_types: Set[str] = temporal_activity_types
        self._backoff = backoff

        self._delay_window_in_seconds = 5 * 60  # 5 min
        self._consecutive_failures = 0
        self._schedule_create_or_update_worker_delay_task: Optional[asyncio.Task] = None
        self._started = False

    async def start(self) -> None:
        if self._started:
            return

        self._started = True
        await self._create_or_update_worker()
        self._schedule_create_or_update_worker()

    async def _create_or_update_worker(self):
        worker_request = models.Worker(
            identity=self._get_worker_identity(),
            hostname=socket.gethostname(),
            ip=self._get_local_ip(),
            task_queue=self._temporal_worker.task_queue,
            workflow_types=list(self._temporal_workflow_types),
            activity_types=list(self._temporal_activity_types),
        )

        try:
            http_response: Any = {}

            def cls(pipeline_response: PipelineResponse, worker: models.Worker, ignored: Dict[str, Any]):
                nonlocal http_response

                http_response = pipeline_response.http_response

                return worker

            worker_response = self._kuflow_client.worker.create_worker(worker_request, cls=cls)
            logger.info(
                f"""
                Registered worker {worker_response.task_queue}/{worker_response.identity} with id {worker_response.id}
                """.strip()
            )

            self._consecutive_failures = 0

            delay_window_header: Optional[str] = http_response.headers["x-kf-delay-window"]
            if delay_window_header is not None:
                self._delay_window_in_seconds = int(delay_window_header)
        except Exception as err:
            self._consecutive_failures = self._consecutive_failures + 1

            logger.error(
                f"There are some problems registering worker {worker_request.task_queue}/{worker_request.identity}", err
            )

    def _schedule_create_or_update_worker(self) -> None:
        delay_window_in_seconds = self._delay_window_in_seconds
        if self._consecutive_failures > 0:
            delay_window_in_seconds = min(
                delay_window_in_seconds,
                round(self._backoff.sleep * self._backoff.exponential_rate**self._consecutive_failures),
            )

        if self._schedule_create_or_update_worker_delay_task:
            self._schedule_create_or_update_worker_delay_task.cancel()
        self._schedule_create_or_update_worker_delay_task = asyncio.create_task(
            self._execute_task__create_or_update_worker(delay_window_in_seconds)
        )

    async def _execute_task__create_or_update_worker(self, delay_in_seconds: float):
        await asyncio.sleep(delay_in_seconds)
        await self._create_or_update_worker()
        self._schedule_create_or_update_worker()

    def _get_worker_identity(self) -> str:
        worker_config = self._temporal_worker.config()
        if worker_config["identity"] is not None:
            return worker_config["identity"]

        return self._temporal_client.identity

    def _get_local_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(("192.255.255.255", 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

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

import asyncio
import logging

import yaml
from _test_workflow import GreetingWorkflow
from temporalio.client import TLSConfig

from kuflow_rest import KuFlowRestClient
from kuflow_temporal_activity_kuflow import KuFlowAsyncActivities, KuFlowSyncActivities
from kuflow_temporal_common.connection import (
    KuFlowConfig,
    KuFlowTemporalConnection,
    TemporalClientConfig,
    TemporalConfig,
    TemporalWorkerConfig,
)

# Load configuration
with open("kuflow-temporal-activity-kuflow/test/application-local.yaml", "r") as file:
    yaml_data = yaml.safe_load(file)

    client_id = yaml_data["kuflow"]["api"]["client-id"]
    client_secret = yaml_data["kuflow"]["api"]["client-secret"]
    endpoint = "https://api.sandbox.kuflow.com/v2022-10-08"  # Overwrite default only for internal testing

    server_root_ca_cert = yaml_data["temporal"]["mutual-tls"]["ca-data"]
    server_root_ca_cert = server_root_ca_cert.encode("utf-8")

    client_cert = yaml_data["temporal"]["mutual-tls"]["cert-data"]
    client_cert = client_cert.encode("utf-8")

    client_key = yaml_data["temporal"]["mutual-tls"]["key-data"]
    client_key = client_key.encode("utf-8")

    temporal_host = yaml_data["temporal"]["target"]
    temporal_namespace = yaml_data["temporal"]["namespace"]
    temporal_queue = yaml_data["temporal"]["kuflow-queue"]


async def main():
    # Uncomment the line below to see logging
    logging.basicConfig(level=logging.INFO)

    kuflow_rest_client = KuFlowRestClient(
        client_id=client_id,
        client_secret=client_secret,
        endpoint=endpoint,
    )

    kuflow_sync_activities = KuFlowSyncActivities(kuflow_rest_client)
    kuflow_async_activities = KuFlowAsyncActivities(kuflow_rest_client)

    activities = kuflow_sync_activities.activities + kuflow_async_activities.activities

    kuflow_temporal_connection = KuFlowTemporalConnection(
        kuflow=KuFlowConfig(rest_client=kuflow_rest_client),
        temporal=TemporalConfig(
            client=TemporalClientConfig(
                target_host=temporal_host,
                namespace=temporal_namespace,
                tls=TLSConfig(
                    server_root_ca_cert=server_root_ca_cert,
                    client_cert=client_cert,
                    client_private_key=client_key,
                ),
            ),
            worker=TemporalWorkerConfig(
                task_queue=temporal_queue,
                workflows=[GreetingWorkflow],
                activities=activities,
                debug_mode=True,
            ),
        ),
    )

    await kuflow_temporal_connection.run_worker()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
import dataclasses
import yaml

from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker
from temporalio.converter import DataConverter

from kuflow_temporal_activity_kuflow.converter import KuFlowPayloadConverter
from kuflow_temporal_common.authentication import KuFlowAuthorizationTokenProvider
from kuflow_rest import KuFlowRestClient
from kuflow_temporal_activity_kuflow import KuFlowAsyncActivities
from kuflow_temporal_activity_kuflow import KuFlowSyncActivities
from _test_workflow import GreetingWorkflow

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

    kuflow_client = KuFlowRestClient(
        client_id=client_id,
        client_secret=client_secret,
        endpoint=endpoint,
        allow_insecure_connection=True,
    )

    # Create an KuFlow token provider
    kuFlow_authorization_token_provider = KuFlowAuthorizationTokenProvider(kuflow_client=kuflow_client)

    client = await Client.connect(
        temporal_host,
        namespace=temporal_namespace,
        tls=TLSConfig(
            server_root_ca_cert=server_root_ca_cert,
            client_cert=client_cert,
            client_private_key=client_key,
        ),
        rpc_metadata=kuFlow_authorization_token_provider.initialize_rpc_auth_metadata(),
        data_converter=dataclasses.replace(
            DataConverter.default,
            payload_converter_class=KuFlowPayloadConverter,
        ),
    )

    kuFlow_authorization_token_provider.start_auto_refresh(client)

    # Run a worker for the workflow
    kuflow_sync_activities = KuFlowSyncActivities(kuflow_client)
    kuflow_async_activities = KuFlowAsyncActivities(kuflow_client)

    worker = Worker(
        client,
        debug_mode=True,  # Debug mode
        task_queue=temporal_queue,
        workflows=[GreetingWorkflow],
        activities=kuflow_sync_activities.activities + kuflow_async_activities.activities,
        # In order to debug in vscode, use UnsandboxedWorkflowRunner "from temporalio.worker":
        #   workflow_runner=UnsandboxedWorkflowRunner()
        # and (optionally if you want set a breakpoint inside Temporal code):
        #   1) Add temporalio package to the workspace to breakpoint inside,
        #   2) Launch with justMyCode": false in launch configuration
        # More info: https://github.com/temporalio/sdk-python/issues/238
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

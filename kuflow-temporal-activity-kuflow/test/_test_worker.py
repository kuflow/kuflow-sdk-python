import asyncio
import logging
import dataclasses

from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker
from temporalio.converter import DataConverter

from kuflow_temporal_activity_kuflow.converter import KuFlowPayloadConverter
from kuflow_temporal_common.authentication import KuFlowAuthorizationTokenProvider
from kuflow_rest import KuFlowRestClient
from kuflow_temporal_activity_kuflow import KuFlowAsyncActivities
from kuflow_temporal_activity_kuflow import KuFlowSyncActivities
from _test_workflow import GreetingWorkflow


async def main():
    # Uncomment the line below to see logging
    logging.basicConfig(level=logging.INFO)

    # MTLS
    with open(
        "/home/zeben/dev/kuflow/src/worker-python-sdk/etc/certs/server-root-ca.cert",
        "rb",
    ) as f:
        server_root_ca_cert = f.read()

    with open("/home/zeben/dev/kuflow/src/worker-python-sdk/etc/certs/client.cert", "rb") as f:
        client_cert = f.read()

    with open("/home/zeben/dev/kuflow/src/worker-python-sdk/etc/certs/client.key", "rb") as f:
        client_key = f.read()

    kuflow_client = KuFlowRestClient(
        client_id=client_id,
        client_secret=client_secret,
        endpoint=endpoint,
        allow_insecure_connection=True,
    )

    # Create an KuFlow token provider
    kuFlow_authorization_token_provider = KuFlowAuthorizationTokenProvider(kuflow_client=kuflow_client)

    client = await Client.connect(
        "engine.sandbox.kuflow.com:443",
        namespace="tenant-d434658f-abe2-491a-b2ef-b073c752617c",
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
        task_queue="greeting-task-queue",
        workflows=[GreetingWorkflow],
        activities=kuflow_sync_activities.activities + kuflow_async_activities.activities,
        # workflow_runner=UnsandboxedWorkflowRunner(),  # Disable Sandboxing in test
    )

    await worker.run()
    # await kuFlow_authorizationToken_provider.close()

    # Run a worker for the workflow
    # async with Worker(
    #     client,
    #     task_queue="greeting-task-queue",
    #     workflows=[GreetingWorkflow],
    #     activities=[compose_greeting, complete_process],
    # ):
    #     # Wait until interrupted
    #     print("Worker started, ctrl+c to exit")
    #     await interrupt_event.wait()
    #     print("Shutting down")

    # async with worker:
    # While the worker is running, use the client to run the workflow and
    # print out its result. Note, in many production setups, the client
    # would be in a completely separate process from the worker.
    # result = await client.execute_workflow(
    #     GreetingWorkflow.run,
    #     "World",
    #     id="hello-activity-workflow-id",
    #     task_queue="greeting-task-queue",
    # )
    # print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
    # loop = asyncio.new_event_loop()
    # try:
    #     loop.run_until_complete(main())
    # except KeyboardInterrupt:
    #     interrupt_event.set()
    #     loop.run_until_complete(loop.shutdown_asyncgens())

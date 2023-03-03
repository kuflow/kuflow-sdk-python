from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

from kuflow_rest import models
from kuflow_temporal_common.activities.kuflow_sync_activities import KuFlowSyncActivities
from kuflow_temporal_common.activities.kuflow_async_activities import KuFlowAsyncActivities
from kuflow_temporal_common.models import _models as models_temporal


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, request: models_temporal.WorkflowRequest) -> models_temporal.WorkflowResponse:
        id = workflow.uuid4()

        task_definition = models.TaskDefinitionSummary(code="T_ONE")
        task = models.Task(id=id, process_id=request.processId, task_definition=task_definition)
        create_task_request = models_temporal.CreateTaskRequest(task=task)

        # Create Task
        await workflow.execute_activity(
            KuFlowAsyncActivities.create_task_and_wait_finished,
            create_task_request,
            start_to_close_timeout=timedelta(days=1),
            schedule_to_close_timeout=timedelta(days=365),
            retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        )

        # result = await workflow.execute_activity(
        #     KuFlowSyncActivities.find_processes,
        #     models_temporal.FindProcessesRequest(size=1),
        #     start_to_close_timeout=timedelta(seconds=120),
        #     retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        # )

        # result = await workflow.execute_activity(
        #     KuFlowSyncActivities.retrieve_principal,
        #     models_temporal.RetrievePrincialRequest(principalId="8934b169-c85e-4e05-9580-13ace7f267f5"),
        #     start_to_close_timeout=timedelta(seconds=120),
        #     retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        # )

        # result = await workflow.execute_activity(
        #     KuFlowSyncActivities.retrieve_process,
        #     models_temporal.RetrieveProcessRequest(request.processId),
        #     start_to_close_timeout=timedelta(seconds=120),
        #     retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        # )

        # Complete Workflow
        result = await workflow.execute_activity(
            KuFlowSyncActivities.complete_process,
            models_temporal.CompleteProcessRequest(request.processId),
            start_to_close_timeout=timedelta(seconds=120),
            retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        )

        return models_temporal.WorkflowResponse(f"Workflow {request.processId} finished")

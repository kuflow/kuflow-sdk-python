from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from kuflow_rest import models
    from kuflow_temporal_activity_kuflow import models as models_temporal
    from kuflow_temporal_activity_kuflow import KuFlowSyncActivities
    from kuflow_temporal_activity_kuflow import KuFlowAsyncActivities


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

        # Complete Workflow
        result = await workflow.execute_activity(
            KuFlowSyncActivities.complete_process,
            models_temporal.CompleteProcessRequest(request.processId),
            start_to_close_timeout=timedelta(seconds=120),
            retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        )

        print(f"Result: {result}")

        return models_temporal.WorkflowResponse(f"Workflow {request.processId} finished")
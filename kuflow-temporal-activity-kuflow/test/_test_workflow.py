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

from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from kuflow_rest import models
    from kuflow_temporal_activity_kuflow import KuFlowAsyncActivities, KuFlowSyncActivities
    from kuflow_temporal_activity_kuflow import models as models_temporal


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, request: models_temporal.WorkflowRequest) -> models_temporal.WorkflowResponse:
        id = workflow.uuid4()

        task_definition = models.TaskDefinitionSummary(code="T_ONE")
        task = models.Task(id=id, process_id=request.process_id, task_definition=task_definition)
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
            models_temporal.CompleteProcessRequest(request.process_id),
            start_to_close_timeout=timedelta(seconds=120),
            retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        )

        workflow.logger.info(f"Result: {result}")

        return models_temporal.WorkflowResponse(f"Workflow {request.process_id} finished")

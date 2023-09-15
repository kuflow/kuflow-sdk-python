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
from typing import List

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from kuflow_rest import models
    from kuflow_temporal_activity_kuflow import KUFLOW_ENGINE_SIGNAL_COMPLETED_TASK, KuFlowActivities
    from kuflow_temporal_activity_kuflow import models as models_temporal


@workflow.defn
class GreetingWorkflow:
    def __init__(self) -> None:
        self._kuflow_completed_task_ids: List[str] = []
        self._exit = False

    @workflow.signal(name=KUFLOW_ENGINE_SIGNAL_COMPLETED_TASK)
    async def kuflow_engine_completed_task(self, task_id: str) -> None:
        self._kuflow_completed_task_ids.append(task_id)

    @workflow.run
    async def run(self, request: models_temporal.WorkflowRequest) -> models_temporal.WorkflowResponse:
        id = workflow.uuid4()

        task_definition = models.TaskDefinitionSummary(code="T_ONE")
        task = models.Task(id=id, process_id=request.process_id, task_definition=task_definition)

        # Create Task
        await self._create_task_and_wait_completion(task)

        workflow.logger.info(f"Finished")

        return models_temporal.WorkflowResponse(f"Workflow {request.process_id} finished")

    async def _create_task_and_wait_completion(self, task: models.Task) -> None:
        create_task_request = models_temporal.CreateTaskRequest(task=task)

        await workflow.execute_activity(
            KuFlowActivities.create_task,
            create_task_request,
            start_to_close_timeout=timedelta(days=1),
            schedule_to_close_timeout=timedelta(days=365),
            retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        )
        await workflow.wait_condition(lambda: task.id in self._kuflow_completed_task_ids)

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

from kuflow_temporal_workflow_kuflow import uuid7


with workflow.unsafe.imports_passed_through():
    from kuflow_rest import models as models_rest
    from kuflow_temporal_activity_kuflow import KuFlowActivities
    from kuflow_temporal_activity_kuflow import models as models_activity
    from kuflow_temporal_workflow_kuflow import models as models_workflow


@workflow.defn
class SampleEngineWorkerLoanWorkflow:
    def __init__(self) -> None:
        self._kuflow_completed_process_item_ids: List[str] = []

    @workflow.signal(name=models_workflow.KUFLOW_ENGINE_SIGNAL_PROCESS_ITEM)
    async def kuflow_engine_signal_process_item(self, signal: models_workflow.SignalProcessItem) -> None:
        if signal.type == models_workflow.SignalProcessItemType.TASK:
            self._kuflow_completed_process_item_ids.append(signal.id)

    @workflow.run
    async def run(self, request: models_workflow.WorkflowRequest) -> models_workflow.WorkflowResponse:
        workflow.logger.info(f"Started {request.process_id}")

        id = str(uuid7())

        process_item_create_request = models_activity.ProcessItemCreateRequest(
            id=id,
            type=models_rest.ProcessItemType.TASK,
            process_id=request.process_id,
            process_item_definition_code="LOAN_APPLICATION",
            task=models_rest.ProcessItemTaskCreateParams(),
        )

        # Create Process Item Task
        await self._create_process_item_and_wait_completion(process_item_create_request)

        workflow.logger.info(f"Finished {request.process_id}")

        return models_workflow.WorkflowResponse(message=f"Workflow {request.process_id} finished")

    async def _create_process_item_and_wait_completion(
        self, create_process_item_request: models_activity.ProcessItemCreateRequest
    ) -> None:
        await workflow.execute_activity(
            KuFlowActivities.create_process_item,
            create_process_item_request,
            start_to_close_timeout=timedelta(days=1),
            schedule_to_close_timeout=timedelta(days=365),
            retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=30)),
        )
        await workflow.wait_condition(lambda: create_process_item_request.id in self._kuflow_completed_process_item_ids)

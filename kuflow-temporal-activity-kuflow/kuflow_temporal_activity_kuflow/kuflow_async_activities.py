import base64

from temporalio import activity
from kuflow_rest import KuFlowRestClient

from . import models as models_temporal


class KuFlowAsyncActivities:
    def __init__(self, kuflow_client: KuFlowRestClient) -> None:
        self._kuflow_client = kuflow_client
        self.activities = [self.create_task_and_wait_finished]

    @activity.defn
    async def create_task_and_wait_finished(
        self,
        request: models_temporal.CreateTaskRequest,
    ) -> None:
        base64_token = base64.b64encode(activity.info().task_token)

        self._kuflow_client.task.create_task(task=request.task, activity_token=base64_token.decode())

        # Raise the complete-async error which will complete this function but
        # does not consider the activity complete from the workflow perspective
        activity.raise_complete_async()

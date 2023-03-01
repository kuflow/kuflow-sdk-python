from temporalio import activity
from ..models import _models as models_temporal

from kuflow_rest import KuFlowRestClient


class KuFlowSyncActivities:
    def __init__(self, kuflow_client: KuFlowRestClient) -> None:
        self._kuflow_client = kuflow_client

    @activity.defn
    async def retrieve_process(
        self,
        request: models_temporal.RetrieveProcessRequest,
    ) -> models_temporal.RetrieveProcessResponse:
        process = self._kuflow_client.process.retrieve_process(id=request.processId)

        return models_temporal.RetrieveProcessResponse(process=process)

    @activity.defn
    async def complete_process(
        self,
        request: models_temporal.CompleteProcessRequest,
    ) -> models_temporal.CompleteProcessResponse:
        process = self._kuflow_client.process.actions_process_complete(request.processId)

        return models_temporal.CompleteProcessResponse(process=process)

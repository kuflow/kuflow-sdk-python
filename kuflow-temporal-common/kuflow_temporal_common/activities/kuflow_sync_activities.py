from temporalio import activity
from ..models import _models as models_temporal

from kuflow_rest import KuFlowRestClient, models


class KuFlowSyncActivities:
    def __init__(self, kuflow_client: KuFlowRestClient) -> None:
        self._kuflow_client = kuflow_client

    @activity.defn
    async def retrieve_principal(
        self,
        request: models_temporal.RetrievePrincialRequest,
    ) -> models_temporal.RetrievePrincialResponse:
        principal = self._kuflow_client.principal.retrieve_principal(id=request.principalId)

        return models_temporal.RetrievePrincialResponse(principal=principal)

    @activity.defn
    async def find_processes(
        self,
        request: models_temporal.FindProcessesRequest,
    ) -> models_temporal.FindProcessesResponse:
        # Get all non-None properties of the object to avoid overwrite defaults
        non_none_props = {k: v for k, v in vars(request).items() if v is not None}

        procesPage = self._kuflow_client.process.find_processes(**non_none_props)

        return models_temporal.FindProcessesResponse(processes=procesPage)

    @activity.defn
    async def retrieve_process(
        self,
        request: models_temporal.RetrieveProcessRequest,
    ) -> models_temporal.RetrieveProcessResponse:
        process = self._kuflow_client.process.retrieve_process(id=request.processId)

        return models_temporal.RetrieveProcessResponse(process=process)

    @activity.defn
    async def save_process_element(
        self,
        request: models_temporal.SaveProcessElementRequest,
    ) -> models_temporal.SaveProcessElementResponse:
        command = models.ProcessSaveElementCommand(
            element_definition_code=request.elementDefinitionCode, element_values=request.elementValues
        )

        process = self._kuflow_client.process.actions_process_save_element(id=request.processId, command=command)

        return models_temporal.SaveProcessElementResponse(process=process)

    @activity.defn
    async def delete_process_element(
        self,
        request: models_temporal.DeleteProcessElementRequest,
    ) -> models_temporal.DeleteProcessElementResponse:
        command = models.ProcessDeleteElementCommand(element_definition_code=request.elementDefinitionCode)

        process = self._kuflow_client.process.actions_process_delete_element(id=request.processId, command=command)

        return models_temporal.DeleteProcessElementResponse(process=process)

    @activity.defn
    async def complete_process(
        self,
        request: models_temporal.CompleteProcessRequest,
    ) -> models_temporal.CompleteProcessResponse:
        process = self._kuflow_client.process.actions_process_complete(request.processId)

        return models_temporal.CompleteProcessResponse(process=process)

    @activity.defn
    async def change_process_initiator(
        self,
        request: models_temporal.ChangeProcessInitiatorRequest,
    ) -> models_temporal.ChangeProcessInitiatorResponse:
        command = models.ProcessChangeInitiatorCommand(email=request.email, principal_id=request.principalId)

        process = self._kuflow_client.process.actions_process_change_initiator(id=request.processId, command=command)

        return models_temporal.ChangeProcessInitiatorResponse(process=process)

    @activity.defn
    async def find_tasks(
        self,
        request: models_temporal.FindTaskRequest,
    ) -> models_temporal.FindTaskResponse:
        # Get all non-None properties of the object to avoid overwrite defaults
        non_none_props = {k: v for k, v in vars(request).items() if v is not None}

        taskPage = self._kuflow_client.task.find_tasks(**non_none_props)

        return models_temporal.FindTaskResponse(tasks=taskPage)

    @activity.defn
    async def retrieve_task(
        self,
        request: models_temporal.RetrieveTaskRequest,
    ) -> models_temporal.RetrieveTaskResponse:
        task = self._kuflow_client.task.retrieve_task(id=request.taskId)

        return models_temporal.RetrieveTaskResponse(task=task)

    @activity.defn
    async def create_task(
        self,
        request: models_temporal.CreateTaskRequest,
    ) -> models_temporal.CreateTaskResponse:
        task = self._kuflow_client.task.create_task(id=request.task)

        return models_temporal.CreateTaskResponse(task=task)

    @activity.defn
    async def complete_task(
        self,
        request: models_temporal.CompleteTaskRequest,
    ) -> models_temporal.CompleteTaskResponse:
        task = self._kuflow_client.task.actions_task_complete(id=request.taskId)

        return models_temporal.CompleteTaskResponse(task=task)

    @activity.defn
    async def claim_task(
        self,
        request: models_temporal.ClaimTaskRequest,
    ) -> models_temporal.CompleteTaskResponse:
        task = self._kuflow_client.task.actions_task_claim(id=request.taskId)

        return models_temporal.ClaimTaskResponse(task=task)

    @activity.defn
    async def assign_task(
        self,
        request: models_temporal.AssignTaskRequest,
    ) -> models_temporal.AssignTaskResponse:
        command = models.TaskAssignCommand(email=request.email, principal_id=request.principalId)

        task = self._kuflow_client.task.actions_task_assign(id=request.taskId, command=command)

        return models_temporal.AssignTaskResponse(task=task)

    @activity.defn
    async def save_task_element(
        self,
        request: models_temporal.SaveTaskElementRequest,
    ) -> models_temporal.SaveTaskElementResponse:
        command = models.TaskSaveElementCommand(
            element_definition_code=request.elementDefinitionCode, element_values=request.elementValues
        )

        task = self._kuflow_client.task.actions_task_save_element(id=request.taskId, command=command)

        return models_temporal.SaveTaskElementResponse(task=task)

    @activity.defn
    async def delete_task_element(
        self,
        request: models_temporal.DeleteTaskElementRequest,
    ) -> models_temporal.DeleteTaskElementResponse:
        command = models.TaskDeleteElementCommand(element_definition_code=request.elementDefinitionCode)

        task = self._kuflow_client.task.actions_task_delete_element(id=request.taskId, command=command)

        return models_temporal.DeleteTaskElementResponse(task=task)

    @activity.defn
    async def delete_task_element_value_document(
        self,
        request: models_temporal.DeleteTaskElementValueDocumentRequest,
    ) -> models_temporal.DeleteTaskElementValueDocumentResponse:
        command = models.TaskDeleteElementValueDocumentCommand(document_id=request.documentId)

        task = self._kuflow_client.task.actions_task_delete_element_value_document(id=request.taskId, command=command)

        return models_temporal.DeleteTaskElementValueDocumentResponse(task=task)

    @activity.defn
    async def append_task_log(
        self,
        request: models_temporal.AppendTaskLogRequest,
    ) -> models_temporal.AppendTaskLogResponse:
        task = self._kuflow_client.task.actions_task_append_log(id=request.taskId, log=request.log)

        return models_temporal.AppendTaskLogResponse(task=task)

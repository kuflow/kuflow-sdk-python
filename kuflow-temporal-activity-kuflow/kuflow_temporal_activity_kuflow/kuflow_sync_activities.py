from temporalio import activity

from kuflow_rest import KuFlowRestClient, models
from kuflow_temporal_activity_kuflow import validation
from kuflow_temporal_common import exceptions

from . import models as models_temporal


class KuFlowSyncActivities:
    def __init__(self, kuflow_client: KuFlowRestClient) -> None:
        self._kuflow_client = kuflow_client
        self.activities = [
            self.retrieve_principal,
            self.find_processes,
            self.retrieve_process,
            self.save_process_element,
            self.delete_process_element,
            self.complete_process,
            self.change_process_initiator,
            self.find_tasks,
            self.retrieve_task,
            self.create_task,
            self.complete_task,
            self.claim_task,
            self.assign_task,
            self.save_task_element,
            self.delete_task_element,
            self.delete_task_element_value_document,
            self.append_task_log,
        ]

    @activity.defn
    async def retrieve_principal(
        self,
        request: models_temporal.RetrievePrincipalRequest,
    ) -> models_temporal.RetrievePrincipalResponse:
        try:
            validation.validate_retrieve_principal_request(request)

            principal = self._kuflow_client.principal.retrieve_principal(id=request.principalId)

            return models_temporal.RetrievePrincipalResponse(principal=principal)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def find_processes(
        self,
        request: models_temporal.FindProcessesRequest,
    ) -> models_temporal.FindProcessesResponse:
        try:
            # Get all non-None properties of the object to avoid overwrite defaults
            non_none_props = {k: v for k, v in vars(request).items() if v is not None}
            procesPage = self._kuflow_client.process.find_processes(**non_none_props)

            return models_temporal.FindProcessesResponse(processes=procesPage)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def retrieve_process(
        self,
        request: models_temporal.RetrieveProcessRequest,
    ) -> models_temporal.RetrieveProcessResponse:
        try:
            validation.validate_retrieve_process_request(request)

            process = self._kuflow_client.process.retrieve_process(id=request.processId)

            return models_temporal.RetrieveProcessResponse(process=process)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def save_process_element(
        self,
        request: models_temporal.SaveProcessElementRequest,
    ) -> models_temporal.SaveProcessElementResponse:
        try:
            validation.validate_save_process_element_request(request)

            command = models.ProcessSaveElementCommand(
                element_definition_code=request.elementDefinitionCode, element_values=request.elementValues
            )
            process = self._kuflow_client.process.actions_process_save_element(id=request.processId, command=command)

            return models_temporal.SaveProcessElementResponse(process=process)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def delete_process_element(
        self,
        request: models_temporal.DeleteProcessElementRequest,
    ) -> models_temporal.DeleteProcessElementResponse:
        try:
            validation.validate_delete_process_element_request(request)

            command = models.ProcessDeleteElementCommand(element_definition_code=request.elementDefinitionCode)

            process = self._kuflow_client.process.actions_process_delete_element(id=request.processId, command=command)

            return models_temporal.DeleteProcessElementResponse(process=process)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def complete_process(
        self,
        request: models_temporal.CompleteProcessRequest,
    ) -> models_temporal.CompleteProcessResponse:
        try:
            validation.validate_complete_process_request(request)

            process = self._kuflow_client.process.actions_process_complete(request.processId)

            return models_temporal.CompleteProcessResponse(process=process)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def change_process_initiator(
        self,
        request: models_temporal.ChangeProcessInitiatorRequest,
    ) -> models_temporal.ChangeProcessInitiatorResponse:
        try:
            validation.validate_change_process_initiator_request(request)

            command = models.ProcessChangeInitiatorCommand(email=request.email, principal_id=request.principalId)
            process = self._kuflow_client.process.actions_process_change_initiator(
                id=request.processId, command=command
            )

            return models_temporal.ChangeProcessInitiatorResponse(process=process)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def find_tasks(
        self,
        request: models_temporal.FindTaskRequest,
    ) -> models_temporal.FindTaskResponse:
        try:
            # Get all non-None properties of the object to avoid overwrite defaults
            non_none_props = {k: v for k, v in vars(request).items() if v is not None}
            taskPage = self._kuflow_client.task.find_tasks(**non_none_props)

            return models_temporal.FindTaskResponse(tasks=taskPage)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def retrieve_task(
        self,
        request: models_temporal.RetrieveTaskRequest,
    ) -> models_temporal.RetrieveTaskResponse:
        try:
            validation.validate_retrieve_task_request(request)

            task = self._kuflow_client.task.retrieve_task(id=request.taskId)

            return models_temporal.RetrieveTaskResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def create_task(
        self,
        request: models_temporal.CreateTaskRequest,
    ) -> models_temporal.CreateTaskResponse:
        try:
            validation.validate_create_task_request(request)

            task = self._kuflow_client.task.create_task(id=request.task)

            return models_temporal.CreateTaskResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def complete_task(
        self,
        request: models_temporal.CompleteTaskRequest,
    ) -> models_temporal.CompleteTaskResponse:
        try:
            validation.validate_complete_task_request(request)

            task = self._kuflow_client.task.actions_task_complete(id=request.taskId)

            return models_temporal.CompleteTaskResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def claim_task(
        self,
        request: models_temporal.ClaimTaskRequest,
    ) -> models_temporal.CompleteTaskResponse:
        try:
            validation.validate_claim_task_request(request)

            task = self._kuflow_client.task.actions_task_claim(id=request.taskId)

            return models_temporal.ClaimTaskResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def assign_task(
        self,
        request: models_temporal.AssignTaskRequest,
    ) -> models_temporal.AssignTaskResponse:
        try:
            validation.validate_assign_task_request(request)

            command = models.TaskAssignCommand(email=request.email, principal_id=request.principalId)
            task = self._kuflow_client.task.actions_task_assign(id=request.taskId, command=command)

            return models_temporal.AssignTaskResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def save_task_element(
        self,
        request: models_temporal.SaveTaskElementRequest,
    ) -> models_temporal.SaveTaskElementResponse:
        try:
            validation.validate_save_task_element_request(request)

            command = models.TaskSaveElementCommand(
                element_definition_code=request.elementDefinitionCode, element_values=request.elementValues
            )
            task = self._kuflow_client.task.actions_task_save_element(id=request.taskId, command=command)

            return models_temporal.SaveTaskElementResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def delete_task_element(
        self,
        request: models_temporal.DeleteTaskElementRequest,
    ) -> models_temporal.DeleteTaskElementResponse:
        try:
            validation.validate_delete_task_element_request(request)

            command = models.TaskDeleteElementCommand(element_definition_code=request.elementDefinitionCode)
            task = self._kuflow_client.task.actions_task_delete_element(id=request.taskId, command=command)

            return models_temporal.DeleteTaskElementResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def delete_task_element_value_document(
        self,
        request: models_temporal.DeleteTaskElementValueDocumentRequest,
    ) -> models_temporal.DeleteTaskElementValueDocumentResponse:
        try:
            validation.validate_delete_task_element_value_document_request(request)

            command = models.TaskDeleteElementValueDocumentCommand(document_id=request.documentId)
            task = self._kuflow_client.task.actions_task_delete_element_value_document(
                id=request.taskId, command=command
            )

            return models_temporal.DeleteTaskElementValueDocumentResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

    @activity.defn
    async def append_task_log(
        self,
        request: models_temporal.AppendTaskLogRequest,
    ) -> models_temporal.AppendTaskLogResponse:
        try:
            validation.validate_append_task_log_request(request)

            task = self._kuflow_client.task.actions_task_append_log(id=request.taskId, log=request.log)

            return models_temporal.AppendTaskLogResponse(task=task)
        except Exception as err:
            return exceptions.create_application_error(err)

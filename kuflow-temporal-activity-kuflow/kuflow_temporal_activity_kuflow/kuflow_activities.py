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

from temporalio import activity

from kuflow_rest import KuFlowRestClient, models
from kuflow_temporal_common import converter, exceptions

from . import _validation as validation
from . import models as models_temporal
from .converter import KuFlowComposableEncodingPayloadConverter


class KuFlowActivities:
    def __init__(self, kuflow_client: KuFlowRestClient) -> None:
        self._kuflow_client = kuflow_client
        self.activities = [
            self.retrieve_principal,
            self.find_processes,
            self.retrieve_process,
            self.save_process_element,
            self.delete_process_element,
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

    @activity.defn(name="KuFlow_Engine_retrievePrincipal")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def retrieve_principal(
        self,
        request: models_temporal.RetrievePrincipalRequest,
    ) -> models_temporal.RetrievePrincipalResponse:
        try:
            validation.validate_retrieve_principal_request(request)

            principal = self._kuflow_client.principal.retrieve_principal(id=request.principal_id)

            return models_temporal.RetrievePrincipalResponse(principal=principal)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_findProcesses")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def find_processes(
        self,
        request: models_temporal.FindProcessesRequest,
    ) -> models_temporal.FindProcessesResponse:
        try:
            # Get all non-None properties of the object to avoid overwrite defaults
            non_none_props = {k: v for k, v in vars(request).items() if v is not None}
            proces_page = self._kuflow_client.process.find_processes(**non_none_props)

            return models_temporal.FindProcessesResponse(processes=proces_page)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_retrieveProcess")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def retrieve_process(
        self,
        request: models_temporal.RetrieveProcessRequest,
    ) -> models_temporal.RetrieveProcessResponse:
        try:
            validation.validate_retrieve_process_request(request)

            process = self._kuflow_client.process.retrieve_process(id=request.process_id)

            return models_temporal.RetrieveProcessResponse(process=process)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_saveProcessElement")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def save_process_element(
        self,
        request: models_temporal.SaveProcessElementRequest,
    ) -> models_temporal.SaveProcessElementResponse:
        try:
            validation.validate_save_process_element_request(request)

            command = models.ProcessSaveElementCommand(
                element_definition_code=request.element_definition_code, element_values=request.element_values
            )
            process = self._kuflow_client.process.actions_process_save_element(id=request.process_id, command=command)

            return models_temporal.SaveProcessElementResponse(process=process)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_deleteProcessElement")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def delete_process_element(
        self,
        request: models_temporal.DeleteProcessElementRequest,
    ) -> models_temporal.DeleteProcessElementResponse:
        try:
            validation.validate_delete_process_element_request(request)

            command = models.ProcessDeleteElementCommand(element_definition_code=request.element_definition_code)

            process = self._kuflow_client.process.actions_process_delete_element(id=request.process_id, command=command)

            return models_temporal.DeleteProcessElementResponse(process=process)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_changeProcessInitiator")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def change_process_initiator(
        self,
        request: models_temporal.ChangeProcessInitiatorRequest,
    ) -> models_temporal.ChangeProcessInitiatorResponse:
        try:
            validation.validate_change_process_initiator_request(request)

            command = models.ProcessChangeInitiatorCommand(email=request.email, principal_id=request.principal_id)
            process = self._kuflow_client.process.actions_process_change_initiator(
                id=request.process_id, command=command
            )

            return models_temporal.ChangeProcessInitiatorResponse(process=process)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_findTasks")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def find_tasks(
        self,
        request: models_temporal.FindTaskRequest,
    ) -> models_temporal.FindTaskResponse:
        try:
            # Get all non-None properties of the object to avoid overwrite defaults
            non_none_props = {k: v for k, v in vars(request).items() if v is not None}
            task_page = self._kuflow_client.task.find_tasks(**non_none_props)

            return models_temporal.FindTaskResponse(tasks=task_page)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_retrieveTask")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def retrieve_task(
        self,
        request: models_temporal.RetrieveTaskRequest,
    ) -> models_temporal.RetrieveTaskResponse:
        try:
            validation.validate_retrieve_task_request(request)

            task = self._kuflow_client.task.retrieve_task(id=request.task_id)

            return models_temporal.RetrieveTaskResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_createTask")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def create_task(
        self,
        request: models_temporal.CreateTaskRequest,
    ) -> models_temporal.CreateTaskResponse:
        try:
            validation.validate_create_task_request(request)

            task = self._kuflow_client.task.create_task(task=request.task)

            return models_temporal.CreateTaskResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_completeTask")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def complete_task(
        self,
        request: models_temporal.CompleteTaskRequest,
    ) -> models_temporal.CompleteTaskResponse:
        try:
            validation.validate_complete_task_request(request)

            task = self._kuflow_client.task.actions_task_complete(id=request.task_id)

            return models_temporal.CompleteTaskResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_claimTask")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def claim_task(
        self,
        request: models_temporal.ClaimTaskRequest,
    ) -> models_temporal.ClaimTaskResponse:
        try:
            validation.validate_claim_task_request(request)

            task = self._kuflow_client.task.actions_task_claim(id=request.task_id)

            return models_temporal.ClaimTaskResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_assignTask")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def assign_task(
        self,
        request: models_temporal.AssignTaskRequest,
    ) -> models_temporal.AssignTaskResponse:
        try:
            validation.validate_assign_task_request(request)

            command = models.TaskAssignCommand(email=request.email, principal_id=request.principal_id)
            task = self._kuflow_client.task.actions_task_assign(id=request.task_id, command=command)

            return models_temporal.AssignTaskResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_saveTaskElement")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def save_task_element(
        self,
        request: models_temporal.SaveTaskElementRequest,
    ) -> models_temporal.SaveTaskElementResponse:
        try:
            validation.validate_save_task_element_request(request)

            command = models.TaskSaveElementCommand(
                element_definition_code=request.element_definition_code, element_values=request.element_values
            )
            task = self._kuflow_client.task.actions_task_save_element(id=request.task_id, command=command)

            return models_temporal.SaveTaskElementResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_deleteTaskElement")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def delete_task_element(
        self,
        request: models_temporal.DeleteTaskElementRequest,
    ) -> models_temporal.DeleteTaskElementResponse:
        try:
            validation.validate_delete_task_element_request(request)

            command = models.TaskDeleteElementCommand(element_definition_code=request.element_definition_code)
            task = self._kuflow_client.task.actions_task_delete_element(id=request.task_id, command=command)

            return models_temporal.DeleteTaskElementResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_deleteTaskElementValueDocument")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def delete_task_element_value_document(
        self,
        request: models_temporal.DeleteTaskElementValueDocumentRequest,
    ) -> models_temporal.DeleteTaskElementValueDocumentResponse:
        try:
            validation.validate_delete_task_element_value_document_request(request)

            command = models.TaskDeleteElementValueDocumentCommand(document_id=request.document_id)
            task = self._kuflow_client.task.actions_task_delete_element_value_document(
                id=request.task_id, command=command
            )

            return models_temporal.DeleteTaskElementValueDocumentResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_saveTaskJsonFormsValueData")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def save_task_json_forms_value_data(
        self,
        request: models_temporal.SaveTaskJsonFormsValueDataRequest,
    ) -> models_temporal.SaveTaskJsonFormsValueDataResponse:
        try:
            validation.validate_save_task_json_forms_value_data(request)

            command = models.TaskSaveJsonFormsValueDataCommand(data=request.data)
            task = self._kuflow_client.task.actions_task_save_json_forms_value_data(id=request.task_id, command=command)

            return models_temporal.SaveTaskJsonFormsValueDataResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

    @activity.defn(name="KuFlow_Engine_appendTaskLog")
    @converter.register(encoding_payload_converter_class=KuFlowComposableEncodingPayloadConverter)
    async def append_task_log(
        self,
        request: models_temporal.AppendTaskLogRequest,
    ) -> models_temporal.AppendTaskLogResponse:
        try:
            validation.validate_append_task_log_request(request)

            task = self._kuflow_client.task.actions_task_append_log(id=request.task_id, log=request.log)

            return models_temporal.AppendTaskLogResponse(task=task)
        except Exception as err:
            raise exceptions.create_application_error(err) from err

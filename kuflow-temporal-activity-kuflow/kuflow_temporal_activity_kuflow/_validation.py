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

from temporalio.exceptions import ApplicationError

from kuflow_temporal_common.exceptions import KuFlowFailureType

from . import models as models_temporal


def validate_retrieve_principal_request(
    request: models_temporal.RetrievePrincipalRequest,
) -> None:
    if not request.principal_id:
        raise ApplicationError(
            "'processId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_retrieve_process_request(
    request: models_temporal.RetrieveProcessRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'processId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_save_process_element_request(
    request: models_temporal.SaveProcessElementRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'processId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.element_definition_code:
        raise ApplicationError(
            "'elementDefinitionCode' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_delete_process_element_request(
    request: models_temporal.DeleteProcessElementRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'processId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.element_definition_code:
        raise ApplicationError(
            "'elementDefinitionCode' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_change_process_initiator_request(
    request: models_temporal.ChangeProcessInitiatorRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'processId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.email and not request.principal_id:
        raise ApplicationError(
            "'email' or 'principalId' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_retrieve_task_request(
    request: models_temporal.RetrieveTaskRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_create_task_request(
    request: models_temporal.CreateTaskRequest,
) -> None:
    if not request.task.id:
        raise ApplicationError(
            "'task.id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.task.process_id:
        raise ApplicationError(
            "'task.process_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.task.task_definition.code:
        raise ApplicationError(
            "'task.taskDefinition.code' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_complete_task_request(
    request: models_temporal.CompleteTaskRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_claim_task_request(
    request: models_temporal.ClaimTaskRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_assign_task_request(
    request: models_temporal.AssignTaskRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.email and not request.principal_id:
        raise ApplicationError(
            "'email' or 'principalId' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_save_task_element_request(
    request: models_temporal.SaveTaskElementRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.element_definition_code:
        raise ApplicationError(
            "'elementDefinitionCode' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_delete_task_element_request(
    request: models_temporal.DeleteTaskElementRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.element_definition_code:
        raise ApplicationError(
            "'elementDefinitionCode' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_delete_task_element_value_document_request(
    request: models_temporal.DeleteTaskElementValueDocumentRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.document_id:
        raise ApplicationError(
            "'documentId' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_save_task_json_forms_value_data(
    request: models_temporal.SaveTaskJsonFormsValueDataRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.data:
        raise ApplicationError(
            "'data' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_append_task_log_request(
    request: models_temporal.AppendTaskLogRequest,
) -> None:
    if not request.task_id:
        raise ApplicationError(
            "'taskId' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.log.level:
        raise ApplicationError(
            "'log.level' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )

    if not request.log.message:
        raise ApplicationError(
            "'log.message' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )

from temporalio.exceptions import ApplicationError

from kuflow_temporal_common.exceptions import KuFlowFailureType

from .models import _models as models_temporal


def validate_retrieve_principal_request(
    request: models_temporal.RetrievePrincipalRequest,
) -> None:
    if not request.principalId:
        raise ApplicationError(
            message="'processId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )


def validate_retrieve_process_request(
    request: models_temporal.RetrieveProcessRequest,
) -> None:
    if not request.processId:
        raise ApplicationError(
            message="'processId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )


def validate_save_process_element_request(
    request: models_temporal.SaveProcessElementRequest,
) -> None:
    if not request.processId:
        raise ApplicationError(
            message="'processId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.elementDefinitionCode:
        raise ApplicationError(
            message="'elementDefinitionCode' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )


def validate_delete_process_element_request(
    request: models_temporal.DeleteProcessElementRequest,
) -> None:
    if not request.processId:
        raise ApplicationError(
            message="'processId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.elementDefinitionCode:
        raise ApplicationError(
            message="'elementDefinitionCode' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )


def validate_complete_process_request(
    request: models_temporal.CompleteProcessRequest,
) -> None:
    if not request.processId:
        raise ApplicationError(
            message="'processId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )


def validate_change_process_initiator_request(
    request: models_temporal.ChangeProcessInitiatorRequest,
) -> None:
    if not request.processId:
        raise ApplicationError(
            message="'processId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.email and not request.principalId:
        raise ApplicationError(
            message="'email' or 'principalId' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )


def validate_retrieve_task_request(
    request: models_temporal.RetrieveTaskRequest,
) -> None:
    if not request.taskId:
        raise ApplicationError(
            message="'taskId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )


def validate_create_task_request(
    request: models_temporal.CreateTaskRequest,
) -> None:
    if not request.task.id:
        raise ApplicationError(
            message="'task.id' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.task.process_id:
        raise ApplicationError(
            message="'task.process_id' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )

    if not request.task.task_definition.code:
        raise ApplicationError(
            message="'task.taskDefinition.code' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )


def validate_complete_task_request(
    request: models_temporal.CompleteTaskRequest,
) -> None:
    if not request.taskId:
        raise ApplicationError(
            message="'taskId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )


def validate_claim_task_request(
    request: models_temporal.ClaimTaskRequest,
) -> None:
    if not request.taskId:
        raise ApplicationError(
            message="'taskId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )


def validate_assign_task_request(
    request: models_temporal.AssignTaskRequest,
) -> None:
    if not request.taskId:
        raise ApplicationError(
            message="'taskId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.email and not request.principalId:
        raise ApplicationError(
            message="'email' or 'principalId' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )


def validate_save_task_element_request(
    request: models_temporal.SaveTaskElementRequest,
) -> None:
    if not request.taskId:
        raise ApplicationError(
            message="'taskId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.elementDefinitionCode:
        raise ApplicationError(
            message="'elementDefinitionCode' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )


def validate_delete_task_element_request(
    request: models_temporal.DeleteTaskElementRequest,
) -> None:
    if not request.taskId:
        raise ApplicationError(
            message="'taskId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.elementDefinitionCode:
        raise ApplicationError(
            message="'elementDefinitionCode' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )


def validate_delete_task_element_value_document_request(
    request: models_temporal.DeleteTaskElementValueDocumentRequest,
) -> None:
    if not request.taskId:
        raise ApplicationError(
            message="'taskId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.documentId:
        raise ApplicationError(
            message="'documentId' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )


def validate_append_task_log_request(
    request: models_temporal.AppendTaskLogRequest,
) -> None:
    if not request.taskId:
        raise ApplicationError(
            message="'taskId' is required", non_retryable=True, type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE
        )

    if not request.log.level:
        raise ApplicationError(
            message="'log.level' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )

    if not request.log.message:
        raise ApplicationError(
            message="'log.message' is required",
            non_retryable=True,
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
        )

from enum import Enum
from azure.core.exceptions import (
    HttpResponseError,
)
from temporalio.exceptions import ApplicationError


class KuFlowFailureType(Enum):
    ACTIVITIES_FAILURE = "KuFlowActivities.Failure"

    ACTIVITIES_REST_FAILURE = "KuFlowActivities.RestFailure"

    ACTIVITIES_VALIDATION_FAILURE = "KuFlowActivities.ValidationFailure"


def create_application_error(e: Exception) -> ApplicationError:
    if isinstance(e, ApplicationError):
        return e

    if isinstance(e, HttpResponseError):
        return ApplicationError(
            message="Rest Invocation error", type=KuFlowFailureType.ACTIVITIES_REST_FAILURE, details=e
        )

    return ApplicationError(message="Invocation error", type=KuFlowFailureType.ACTIVITIES_FAILURE, details=e)

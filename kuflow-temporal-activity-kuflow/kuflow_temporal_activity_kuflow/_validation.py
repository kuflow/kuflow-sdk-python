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

from kuflow_rest import models as models_rest
from kuflow_temporal_common import KuFlowFailureType

from . import models as models_temporal


def validate_retrieve_principal_request(
    request: models_temporal.PrincipalRetrieveRequest,
) -> None:
    if not request.principal_id:
        raise ApplicationError(
            "'principal_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_retrieve_tenant_user_request(
    request: models_temporal.TenantUserRetrieveRequest,
) -> None:
    if not request.tenant_user_id:
        raise ApplicationError(
            "'tenant_user_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_retrieve_process_request(
    request: models_temporal.ProcessRetrieveRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'process_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_process_entity_update_request(
    request: models_temporal.ProcessEntityUpdateRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'process_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.entity:
        raise ApplicationError(
            "'entity' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_process_entity_patch_request(
    request: models_temporal.ProcessEntityPatchRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'process_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.json_patch:
        raise ApplicationError(
            "'json_patch' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_process_metadata_update_request(
    request: models_temporal.ProcessMetadataUpdateRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'process_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.metadata:
        raise ApplicationError(
            "'metadata' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_process_metadata_patch_request(
    request: models_temporal.ProcessMetadataPatchRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'process_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.json_patch:
        raise ApplicationError(
            "'json_patch' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_process_initiator_change_request(
    request: models_temporal.ProcessInitiatorChangeRequest,
) -> None:
    if not request.process_id:
        raise ApplicationError(
            "'process_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.initiator_id and not request.initiator_email:
        raise ApplicationError(
            "'initiator_id' or 'initiator_email' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_process_item_retrieve_request(
    request: models_temporal.ProcessItemRetrieveRequest,
) -> None:
    if not request.process_item_id:
        raise ApplicationError(
            "'process_item_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_process_item_create_request(
    request: models_temporal.ProcessItemCreateRequest,
) -> None:
    if not request.id:
        raise ApplicationError(
            "'id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.process_id:
        raise ApplicationError(
            "'process_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.type:
        raise ApplicationError(
            "'type' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if request.type is models_rest.ProcessItemType.TASK:
        if not request.process_item_definition_code:
            raise ApplicationError(
                "'process_item_definition_code' is required",
                type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
                non_retryable=True,
            )

    if request.type is models_rest.ProcessItemType.MESSAGE:
        if not request.message:
            raise ApplicationError(
                "'message' is required",
                type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
                non_retryable=True,
            )

        if not request.message.text and not request.message.data:
            raise ApplicationError(
                "'message.text' and/or 'message.data' is required for message items",
                type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
                non_retryable=True,
            )

        if request.message.data and not request.message.data_structure_data_definition_code:
            raise ApplicationError(
                "'message.dataStructureDataDefinitionCode' is required for message items when 'message.data' is set",
                type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
                non_retryable=True,
            )

    if request.type is models_rest.ProcessItemType.THREAD:
        if not request.process_item_definition_code:
            raise ApplicationError(
                "'processItemDefinitionCode' is required for thread items",
                type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
                non_retryable=True,
            )


def validate_process_item_task_complete_request(
    request: models_temporal.ProcessItemTaskCompleteRequest,
) -> None:
    if not request.process_item_id:
        raise ApplicationError(
            "'process_item_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_process_item_task_claim_request(
    request: models_temporal.ProcessItemTaskClaimRequest,
) -> None:
    if not request.process_item_id:
        raise ApplicationError(
            "'process_item_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )


def validate_process_item_task_assign_request(
    request: models_temporal.ProcessItemTaskAssignRequest,
) -> None:
    if not request.process_item_id:
        raise ApplicationError(
            "'process_item_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.owner_id and not request.owner_email:
        raise ApplicationError(
            "'owner_id' or 'owner_email' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_process_item_task_data_update_request(
    request: models_temporal.ProcessItemTaskDataUpdateRequest,
) -> None:
    if not request.process_item_id:
        raise ApplicationError(
            "'process_item_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.data:
        raise ApplicationError(
            "'data' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_process_item_task_data_patch_request(
    request: models_temporal.ProcessItemTaskDataPatchRequest,
) -> None:
    if not request.process_item_id:
        raise ApplicationError(
            "'process_item_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.json_patch:
        raise ApplicationError(
            "'json_patch' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )


def validate_process_item_task_log_append_request(
    request: models_temporal.ProcessItemTaskLogAppendRequest,
) -> None:
    if not request.process_item_id:
        raise ApplicationError(
            "'process_item_id' is required", type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE, non_retryable=True
        )

    if not request.level:
        raise ApplicationError(
            "'level' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )

    if not request.message:
        raise ApplicationError(
            "'message' is required",
            type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            non_retryable=True,
        )

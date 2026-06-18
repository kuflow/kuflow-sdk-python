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

from typing import Any, Optional

from kuflow_rest import models as models_rest
from kuflow_rest._generated._utils import serialization


class PrincipalRetrieveRequest(serialization.Model):
    _attribute_map = {
        "principal_id": {"key": "principalId", "type": "str"},
    }

    def __init__(self, principal_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            principal_id: Identifier of the requested principal
        """
        super().__init__(**kwargs)
        self.principal_id = principal_id


class PrincipalRetrieveResponse(serialization.Model):
    _attribute_map = {
        "principal": {"key": "principal", "type": "Principal"},
    }

    def __init__(self, principal: models_rest.Principal, **kwargs: Any) -> None:
        """
        Parameters:
            principal: Principal data requested
        """
        super().__init__(**kwargs)
        self.principal = principal


class TenantUserRetrieveRequest(serialization.Model):
    _attribute_map = {
        "tenant_user_id": {"key": "tenantUserId", "type": "str"},
    }

    def __init__(self, tenant_user_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            tenant_user_id: Identifier of the requested tenant user
        """
        super().__init__(**kwargs)
        self.tenant_user_id = tenant_user_id


class TenantUserRetrieveResponse(serialization.Model):
    _attribute_map = {
        "tenant_user": {"key": "tenantUser", "type": "Principal"},
    }

    def __init__(self, tenant_user: models_rest.TenantUser, **kwargs: Any) -> None:
        """
        Parameters:
            tenant_user: tenant_user data requested
        """
        super().__init__(**kwargs)
        self.tenant_user = tenant_user


class ProcessFindRequest(serialization.Model):
    _attribute_map = {
        "page": {"key": "page", "type": "int"},
        "size": {"key": "size", "type": "int"},
        "sorts": {"key": "sorts", "type": "[str]"},
    }

    def __init__(
        self, page: Optional[int] = None, size: Optional[int] = None, sorts: Optional[list[str]] = None, **kwargs: Any
    ) -> None:
        """
        Parameters:
            page: Page requested, 0-index
            size: Page size
            sorts: Sorting criteria in the format: property{,asc|desc}. Example: name,desc
        """
        super().__init__(**kwargs)
        self.page = page
        self.size = size
        self.sorts = sorts


class ProcessFindResponse(serialization.Model):
    _attribute_map = {
        "processes": {"key": "processes", "type": "ProcessPage"},
    }

    def __init__(self, processes: models_rest.ProcessPage, **kwargs: Any) -> None:
        """
        Parameters:
            processes: Process page that math the requested criteria
        """
        super().__init__(**kwargs)
        self.processes = processes


class ProcessRetrieveRequest(serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
    }

    def __init__(self, process_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_id: Process Identifier to retrieve
        """
        super().__init__(**kwargs)
        self.process_id = process_id


class ProcessRetrieveResponse(serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process, **kwargs: Any) -> None:
        """
        Parameters:
            process: Requested process data
        """
        super().__init__(**kwargs)
        self.process = process


class ProcessEntityUpdateRequest(serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "entity": {"key": "entity", "type": "JsonValue"},
    }

    def __init__(
        self,
        process_id: str,
        entity: models_rest.JsonValue,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_id: Process identifier to update
            entity: Json value. Required.
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.entity = entity


class ProcessEntityUpdateResponse(serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process, **kwargs: Any) -> None:
        """
        Parameters:
            process: Process updated
        """
        super().__init__(**kwargs)
        self.process = process


class ProcessEntityPatchRequest(serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "json_patch": {"key": "jsonPatch", "type": "[JsonPatchOperation]"},
    }

    def __init__(
        self,
        process_id: str,
        json_patch: list[models_rest.JsonPatchOperation],
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_id: Process identifier to update
            json_patch: Params to patch process entity
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.json_patch = json_patch


class ProcessEntityPatchResponse(serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process, **kwargs: Any) -> None:
        """
        Parameters:
            process: Process updated
        """
        super().__init__(**kwargs)
        self.process = process


class ProcessMetadataUpdateRequest(serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "metadata": {"key": "metadata", "type": "JsonValue"},
    }

    def __init__(
        self,
        process_id: str,
        metadata: models_rest.JsonValue,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_id: Process identifier to update
            metadata: Json value. Required.
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.metadata = metadata


class ProcessMetadataUpdateResponse(serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process, **kwargs: Any) -> None:
        """
        Parameters:
            process: Process updated
        """
        super().__init__(**kwargs)
        self.process = process


class ProcessMetadataPatchRequest(serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "json_patch": {"key": "params", "type": "[JsonPatchOperation]"},
    }

    def __init__(
        self,
        process_id: str,
        json_patch: list[models_rest.JsonPatchOperation],
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_id: Process identifier to update
            json_patch: Params to patch process entity
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.json_patch = json_patch


class ProcessMetadataPatchResponse(serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process, **kwargs: Any) -> None:
        """
        Parameters:
            process: Process updated
        """
        super().__init__(**kwargs)
        self.process = process


class ProcessInitiatorChangeRequest(serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "initiator_id": {"key": "initiatorId", "type": "str"},
        "initiator_email": {"key": "initiatorEmail", "type": "str"},
    }

    def __init__(
        self, process_id: str, initiator_id: Optional[str] = None, initiator_email: Optional[str] = None, **kwargs: Any
    ) -> None:
        """
        Parameters:
            process_id: Process identifier to which want to change the initiator
            initiator_id: Initiator id that wants to use to assign the process.
                          Attribute :initiator_id or :initiator_email must be set.
            initiator_email: User email that wants to use to assign the process. Attribute :initiator_id or
                             :initiator_email must be set.
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.initiator_id = initiator_id
        self.initiator_email = initiator_email


class ProcessInitiatorChangeResponse(serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process, **kwargs: Any) -> None:
        """
        Parameters:
            process: Process updated
        """
        super().__init__(**kwargs)
        self.process = process


class ProcessItemFindRequest(serialization.Model):
    _attribute_map = {
        "page": {"key": "page", "type": "int"},
        "size": {"key": "size", "type": "int"},
        "sorts": {"key": "sorts", "type": "[str]"},
        "tenant_ids": {"key": "tenantIds", "type": "[str]"},
        "process_ids": {"key": "processIds", "type": "[str]"},
        "types": {"key": "types", "type": "[ProcessItemType]"},
        "task_states": {"key": "taskStates", "type": "[ProcessItemTaskState]"},
        "process_item_definition_codes": {"key": "processItemDefinitionCodes", "type": "[str]"},
        "process_definition_ids": {"key": "processDefinitionIds", "type": "[str]"},
        "process_definition_codes": {"key": "processDefinitionCodes", "type": "[str]"},
    }

    def __init__(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        sorts: Optional[list[str]] = None,
        tenant_ids: Optional[list[str]] = None,
        process_ids: Optional[list[str]] = None,
        types: Optional[list[models_rest.ProcessItemType]] = None,
        task_states: Optional[list[models_rest.ProcessItemTaskState]] = None,
        process_item_definition_codes: Optional[list[str]] = None,
        process_definition_ids: Optional[list[str]] = None,
        process_definition_codes: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            page: Page requested, 0-index
            size: Page size
            sorts: Sorting criteria in the format: property{,asc|desc}. Example: name,desc
            tenant_ids: Filter process items by tenant identifiers
            process_ids: Filter process items  by the process identifiers
            types: Filter process items by the types
            task_states: Filter process items by the task states
            process_item_definition_codes: Filter process items by the process item definition codes
            process_definition_ids: Filter process items by the process definition identifiers
            process_definition_codes: Filter process items by the process definition codes
        """
        super().__init__(**kwargs)
        self.page = page
        self.size = size
        self.sorts = sorts
        self.tenant_ids = tenant_ids
        self.process_ids = process_ids
        self.types = types
        self.task_states = task_states
        self.process_item_definition_codes = process_item_definition_codes
        self.process_definition_ids = process_definition_ids
        self.process_definition_codes = process_definition_codes


class ProcessItemFindResponse(serialization.Model):
    _attribute_map = {
        "process_items": {"key": "processItems", "type": "ProcessItemPage"},
    }

    def __init__(self, process_items: models_rest.ProcessItemPage, **kwargs: Any) -> None:
        """
        Parameters:
            process_items: Process Item page that math the requested criteria
        """
        super().__init__(**kwargs)
        self.process_items = process_items


class ProcessItemRetrieveRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
    }

    def __init__(self, process_item_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_item_id: Process Item identifier to retrieve
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id


class ProcessItemRetrieveResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item data
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemCreateRequest(serialization.Model):
    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "type": {"key": "type", "type": "ProcessItemType"},
        "process_id": {"key": "processId", "type": "str"},
        "owner_id": {"key": "ownerId", "type": "str"},
        "owner_email": {"key": "ownerEmail", "type": "str"},
        "process_item_definition_code": {"key": "processItemDefinitionCode", "type": "str"},
        "task": {"key": "task", "type": "ProcessItemTaskCreateParams"},
        "message": {"key": "message", "type": "ProcessItemMessageCreateParams"},
    }

    def __init__(
        self,
        id: str,
        type: models_rest.ProcessItemType,
        process_id: str,
        owner_id: Optional[str] = None,
        owner_email: Optional[str] = None,
        process_item_definition_code: Optional[str] = None,
        task: Optional[models_rest.ProcessItemTaskCreateParams] = None,
        message: Optional[models_rest.ProcessItemMessageCreateParams] = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            id: Process item task id
            type: Process item task type
            process_id: Process id in which create the process item
            owner_id: Owner id, only owner_id or owner_email is allowed
            owner_email: Owner email, only owner_id or owner_email is allowed
            process_item_definition_code: Process Item Task details
            task: Process Item Task details
            message: Process Item Message details
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.process_id = process_id
        self.owner_id = owner_id
        self.owner_email = owner_email
        self.process_item_definition_code = process_item_definition_code
        self.task = task
        self.message = message


class ProcessItemCreateResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item created
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemTaskCompleteRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
    }

    def __init__(self, process_item_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_item_id: Process Item identifier to mark as completed
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id


class ProcessItemTaskCompleteResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item updated
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemTaskClaimRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
    }

    def __init__(self, process_item_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_item_id: Task identifier to claim by the requestor
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id


class ProcessItemTaskClaimResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item claimed
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemTaskAssignRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
        "owner_email": {"key": "ownerEmail", "type": "str"},
        "owner_id": {"key": "ownerId", "type": "str"},
    }

    def __init__(
        self, process_item_id: str, owner_email: Optional[str] = None, owner_id: Optional[str] = None, **kwargs: Any
    ) -> None:
        """
        Parameters:
            process_item_id: Task to assign to the email or principal_id selected
            owner_email: User email that want to use to assign the task. Attribute owner_email or owner_id must be set
            owner_id: Principal id that want to use to assign the task. Attribute owner_email or owner_id must be set
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id
        self.owner_email = owner_email
        self.owner_id = owner_id


class ProcessItemTaskAssignResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item updated
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemTaskDataUpdateRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
        "data": {"key": "data", "type": "JsonValue"},
    }

    def __init__(
        self,
        process_item_id: str,
        data: models_rest.JsonValue,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_item_id: Task to update
            data: Json value. Required.
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id
        self.data = data


class ProcessItemTaskDataUpdateResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item updated
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemTaskDataPatchRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
        "json_patch": {"key": "jsonPatch", "type": "[JsonPatchOperation]"},
    }

    def __init__(
        self,
        process_item_id: str,
        json_patch: list[models_rest.JsonPatchOperation],
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_item_id: Task to update
            json_patch: Params to patch process item task data
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id
        self.json_patch = json_patch


class ProcessItemTaskDataPatchResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item updated
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemTaskLogAppendRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
        "message": {"key": "message", "type": "str"},
        "level": {"key": "level", "type": "ProcessItemTaskLogLevel"},
    }

    def __init__(
        self, process_item_id: str, message: str, level: models_rest.ProcessItemTaskLogLevel, **kwargs: Any
    ) -> None:
        """
        Parameters:
            process_item_id: Task to update
            message: Log message
            level: Log level
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id
        self.message = message
        self.level = level


class ProcessItemTaskLogAppendResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item updated
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemTaskContextDataUpdateRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
        "data": {"key": "data", "type": "JsonValue"},
    }

    def __init__(
        self,
        process_item_id: str,
        data: models_rest.JsonValue,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_item_id: Task to update
            data: Json value. Required.
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id
        self.data = data


class ProcessItemTaskContextDataUpdateResponse(serialization.Model):
    _attribute_map = {
        "process_item": {"key": "processItem", "type": "ProcessItem"},
    }

    def __init__(self, process_item: models_rest.ProcessItem, **kwargs: Any) -> None:
        """
        Parameters:
            process_item: Process Item updated
        """
        super().__init__(**kwargs)
        self.process_item = process_item


class ProcessItemAiAssistanceGenerateRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
        "request_id": {"key": "requestId", "type": "str"},
    }

    def __init__(self, process_item_id: str, request_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_item_id: Process Item to generate AI assistance for
            request_id: Client-supplied identifier (UUID) that makes the call idempotent
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id
        self.request_id = request_id


class ProcessItemAiAssistanceGenerateResponse(serialization.Model):
    _attribute_map = {
        "process_item_ai_assistance": {"key": "processItemAiAssistance", "type": "ProcessItemAiAssistance"},
    }

    def __init__(self, process_item_ai_assistance: models_rest.ProcessItemAiAssistance, **kwargs: Any) -> None:
        """
        Parameters:
            process_item_ai_assistance: Current state of the AI assistance run
        """
        super().__init__(**kwargs)
        self.process_item_ai_assistance = process_item_ai_assistance


class ProcessItemAiAssistanceRetrieveRequest(serialization.Model):
    _attribute_map = {
        "process_item_id": {"key": "processItemId", "type": "str"},
    }

    def __init__(self, process_item_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_item_id: Process Item to retrieve AI assistance for
        """
        super().__init__(**kwargs)
        self.process_item_id = process_item_id


class ProcessItemAiAssistanceRetrieveResponse(serialization.Model):
    _attribute_map = {
        "process_item_ai_assistance": {"key": "processItemAiAssistance", "type": "ProcessItemAiAssistance"},
    }

    def __init__(self, process_item_ai_assistance: models_rest.ProcessItemAiAssistance, **kwargs: Any) -> None:
        """
        Parameters:
            process_item_ai_assistance: Latest persisted AI assistance run
        """
        super().__init__(**kwargs)
        self.process_item_ai_assistance = process_item_ai_assistance


class ProcessItemsCancelRequest(serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "process_item_ids": {"key": "processItemIds", "type": "[str]"},
    }

    def __init__(self, process_id: str, process_item_ids: Optional[list[str]] = None, **kwargs: Any) -> None:
        """
        Parameters:
            process_id: Process whose items are going to be cancelled
            process_item_ids: Optional list of process item IDs to cancel. If omitted, all active
                              process items are cancelled.
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.process_item_ids = process_item_ids


class ProcessItemsCancelResponse(serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process, **kwargs: Any) -> None:
        """
        Parameters:
            process: Process updated
        """
        super().__init__(**kwargs)
        self.process = process


class BusinessArtifactFindRequest(serialization.Model):
    _attribute_map = {
        "page": {"key": "page", "type": "int"},
        "size": {"key": "size", "type": "int"},
        "sorts": {"key": "sorts", "type": "[str]"},
        "tenant_ids": {"key": "tenantIds", "type": "[str]"},
        "business_artifact_definition_ids": {"key": "businessArtifactDefinitionIds", "type": "[str]"},
        "business_artifact_definition_codes": {"key": "businessArtifactDefinitionCodes", "type": "[str]"},
        "values": {"key": "values", "type": "[str]"},
    }

    def __init__(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        sorts: Optional[list[str]] = None,
        tenant_ids: Optional[list[str]] = None,
        business_artifact_definition_ids: Optional[list[str]] = None,
        business_artifact_definition_codes: Optional[list[str]] = None,
        values: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            page: Page requested, 0-index
            size: Page size
            sorts: Sorting criteria in the format: property{,asc|desc}. Example: createdAt,desc
            tenant_ids: Filter business artifacts by tenant identifiers
            business_artifact_definition_ids: Filter by an array of business artifact definition ids
            business_artifact_definition_codes: Filter by an array of business artifact definition codes
            values: Filter by an array of values
        """
        super().__init__(**kwargs)
        self.page = page
        self.size = size
        self.sorts = sorts
        self.tenant_ids = tenant_ids
        self.business_artifact_definition_ids = business_artifact_definition_ids
        self.business_artifact_definition_codes = business_artifact_definition_codes
        self.values = values


class BusinessArtifactFindResponse(serialization.Model):
    _attribute_map = {
        "business_artifacts": {"key": "businessArtifacts", "type": "BusinessArtifactPage"},
    }

    def __init__(self, business_artifacts: models_rest.BusinessArtifactPage, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifacts: Business Artifact page that match the requested criteria
        """
        super().__init__(**kwargs)
        self.business_artifacts = business_artifacts


class BusinessArtifactCreateRequest(serialization.Model):
    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "business_artifact_definition_id": {"key": "businessArtifactDefinitionId", "type": "str"},
        "tenant_id": {"key": "tenantId", "type": "str"},
        "business_artifact_definition_code": {"key": "businessArtifactDefinitionCode", "type": "str"},
        "data": {"key": "data", "type": "JsonValue"},
    }

    def __init__(
        self,
        id: Optional[str] = None,
        business_artifact_definition_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        business_artifact_definition_code: Optional[str] = None,
        data: Optional[models_rest.JsonValue] = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            id: Business Artifact id. Set it to make the call idempotent
            business_artifact_definition_id: Business artifact definition id. Only one of
                                             business_artifact_definition_id or
                                             business_artifact_definition_code is allowed
            tenant_id: Tenant id
            business_artifact_definition_code: Business artifact definition code. Only one of
                                               business_artifact_definition_id or
                                               business_artifact_definition_code is allowed
            data: Json value
        """
        super().__init__(**kwargs)
        self.id = id
        self.business_artifact_definition_id = business_artifact_definition_id
        self.tenant_id = tenant_id
        self.business_artifact_definition_code = business_artifact_definition_code
        self.data = data


class BusinessArtifactCreateResponse(serialization.Model):
    _attribute_map = {
        "business_artifact": {"key": "businessArtifact", "type": "BusinessArtifact"},
    }

    def __init__(self, business_artifact: models_rest.BusinessArtifact, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact: Business Artifact created
        """
        super().__init__(**kwargs)
        self.business_artifact = business_artifact


class BusinessArtifactRetrieveRequest(serialization.Model):
    _attribute_map = {
        "business_artifact_id": {"key": "businessArtifactId", "type": "str"},
    }

    def __init__(self, business_artifact_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_id: Business Artifact identifier to retrieve
        """
        super().__init__(**kwargs)
        self.business_artifact_id = business_artifact_id


class BusinessArtifactRetrieveResponse(serialization.Model):
    _attribute_map = {
        "business_artifact": {"key": "businessArtifact", "type": "BusinessArtifact"},
    }

    def __init__(self, business_artifact: models_rest.BusinessArtifact, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact: Business Artifact data
        """
        super().__init__(**kwargs)
        self.business_artifact = business_artifact


class BusinessArtifactDeleteRequest(serialization.Model):
    _attribute_map = {
        "business_artifact_id": {"key": "businessArtifactId", "type": "str"},
    }

    def __init__(self, business_artifact_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_id: Business Artifact identifier to delete
        """
        super().__init__(**kwargs)
        self.business_artifact_id = business_artifact_id


class BusinessArtifactDeleteResponse(serialization.Model):
    _attribute_map: dict[str, Any] = {}

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class BusinessArtifactUpdateRequest(serialization.Model):
    _attribute_map = {
        "business_artifact_id": {"key": "businessArtifactId", "type": "str"},
        "data": {"key": "data", "type": "JsonValue"},
    }

    def __init__(self, business_artifact_id: str, data: models_rest.JsonValue, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_id: Business Artifact identifier to update
            data: Json value. Required.
        """
        super().__init__(**kwargs)
        self.business_artifact_id = business_artifact_id
        self.data = data


class BusinessArtifactUpdateResponse(serialization.Model):
    _attribute_map = {
        "business_artifact": {"key": "businessArtifact", "type": "BusinessArtifact"},
    }

    def __init__(self, business_artifact: models_rest.BusinessArtifact, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact: Business Artifact updated
        """
        super().__init__(**kwargs)
        self.business_artifact = business_artifact


class BusinessArtifactPatchRequest(serialization.Model):
    _attribute_map = {
        "business_artifact_id": {"key": "businessArtifactId", "type": "str"},
        "json_patch": {"key": "jsonPatch", "type": "[JsonPatchOperation]"},
    }

    def __init__(
        self, business_artifact_id: str, json_patch: list[models_rest.JsonPatchOperation], **kwargs: Any
    ) -> None:
        """
        Parameters:
            business_artifact_id: Business Artifact identifier to update
            json_patch: Params to patch business artifact data
        """
        super().__init__(**kwargs)
        self.business_artifact_id = business_artifact_id
        self.json_patch = json_patch


class BusinessArtifactPatchResponse(serialization.Model):
    _attribute_map = {
        "business_artifact": {"key": "businessArtifact", "type": "BusinessArtifact"},
    }

    def __init__(self, business_artifact: models_rest.BusinessArtifact, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact: Business Artifact updated
        """
        super().__init__(**kwargs)
        self.business_artifact = business_artifact


class BusinessArtifactActionCreateRequest(serialization.Model):
    _attribute_map = {
        "business_artifact_id": {"key": "businessArtifactId", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "business_artifact_action_definition_code": {"key": "businessArtifactActionDefinitionCode", "type": "str"},
        "start_workflow": {"key": "startWorkflow", "type": "BusinessArtifactActionCreateParamsStartWorkflow"},
        "downloadable": {"key": "downloadable", "type": "BusinessArtifactActionCreateParamsDownloadable"},
        "start_process": {"key": "startProcess", "type": "BusinessArtifactActionCreateParamsStartProcess"},
        "create_artifact": {"key": "createArtifact", "type": "BusinessArtifactActionCreateParamsCreateArtifact"},
    }

    def __init__(
        self,
        business_artifact_id: str,
        business_artifact_action_definition_code: str,
        id: Optional[str] = None,
        start_workflow: Optional[models_rest.BusinessArtifactActionCreateParamsStartWorkflow] = None,
        downloadable: Optional[models_rest.BusinessArtifactActionCreateParamsDownloadable] = None,
        start_process: Optional[models_rest.BusinessArtifactActionCreateParamsStartProcess] = None,
        create_artifact: Optional[models_rest.BusinessArtifactActionCreateParamsCreateArtifact] = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            business_artifact_id: Business Artifact on which invoke the action
            business_artifact_action_definition_code: Business artifact action definition code
            id: Business Artifact action id. Set it to make the call idempotent
            start_workflow: Params for a START_WORKFLOW action
            downloadable: Params for a DOWNLOADABLE action
            start_process: Params for a START_PROCESS action
            create_artifact: Params for a CREATE_BUSINESS_ARTIFACT action
        """
        super().__init__(**kwargs)
        self.business_artifact_id = business_artifact_id
        self.business_artifact_action_definition_code = business_artifact_action_definition_code
        self.id = id
        self.start_workflow = start_workflow
        self.downloadable = downloadable
        self.start_process = start_process
        self.create_artifact = create_artifact


class BusinessArtifactActionCreateResponse(serialization.Model):
    _attribute_map = {
        "business_artifact_action": {"key": "businessArtifactAction", "type": "BusinessArtifactAction"},
    }

    def __init__(self, business_artifact_action: models_rest.BusinessArtifactAction, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_action: Business Artifact action invoked
        """
        super().__init__(**kwargs)
        self.business_artifact_action = business_artifact_action


class BusinessArtifactActionRetrieveRequest(serialization.Model):
    _attribute_map = {
        "business_artifact_id": {"key": "businessArtifactId", "type": "str"},
        "business_artifact_action_id": {"key": "businessArtifactActionId", "type": "str"},
    }

    def __init__(self, business_artifact_id: str, business_artifact_action_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_id: Business Artifact identifier
            business_artifact_action_id: Business Artifact action identifier to retrieve
        """
        super().__init__(**kwargs)
        self.business_artifact_id = business_artifact_id
        self.business_artifact_action_id = business_artifact_action_id


class BusinessArtifactActionRetrieveResponse(serialization.Model):
    _attribute_map = {
        "business_artifact_action": {"key": "businessArtifactAction", "type": "BusinessArtifactAction"},
    }

    def __init__(self, business_artifact_action: models_rest.BusinessArtifactAction, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_action: Business Artifact action data
        """
        super().__init__(**kwargs)
        self.business_artifact_action = business_artifact_action


class BusinessArtifactActionCancelRequest(serialization.Model):
    _attribute_map = {
        "business_artifact_id": {"key": "businessArtifactId", "type": "str"},
        "business_artifact_action_id": {"key": "businessArtifactActionId", "type": "str"},
    }

    def __init__(self, business_artifact_id: str, business_artifact_action_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_id: Business Artifact identifier
            business_artifact_action_id: Business Artifact action identifier to cancel
        """
        super().__init__(**kwargs)
        self.business_artifact_id = business_artifact_id
        self.business_artifact_action_id = business_artifact_action_id


class BusinessArtifactActionCancelResponse(serialization.Model):
    _attribute_map = {
        "business_artifact_action": {"key": "businessArtifactAction", "type": "BusinessArtifactAction"},
    }

    def __init__(self, business_artifact_action: models_rest.BusinessArtifactAction, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_action: Business Artifact action cancelled
        """
        super().__init__(**kwargs)
        self.business_artifact_action = business_artifact_action


class BusinessArtifactCreateArtifactPrepareRequest(serialization.Model):
    _attribute_map = {
        "business_artifact_id": {"key": "businessArtifactId", "type": "str"},
        "business_artifact_action_definition_code": {"key": "businessArtifactActionDefinitionCode", "type": "str"},
    }

    def __init__(self, business_artifact_id: str, business_artifact_action_definition_code: str, **kwargs: Any) -> None:
        """
        Parameters:
            business_artifact_id: Business Artifact identifier
            business_artifact_action_definition_code: CREATE_BUSINESS_ARTIFACT action definition code to prepare
        """
        super().__init__(**kwargs)
        self.business_artifact_id = business_artifact_id
        self.business_artifact_action_definition_code = business_artifact_action_definition_code


class BusinessArtifactCreateArtifactPrepareResponse(serialization.Model):
    _attribute_map = {
        "business_artifact_create_artifact_prepare": {
            "key": "businessArtifactCreateArtifactPrepare",
            "type": "BusinessArtifactCreateArtifactPrepare",
        },
    }

    def __init__(
        self,
        business_artifact_create_artifact_prepare: models_rest.BusinessArtifactCreateArtifactPrepare,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            business_artifact_create_artifact_prepare: Prepared data for the CREATE_BUSINESS_ARTIFACT action
        """
        super().__init__(**kwargs)
        self.business_artifact_create_artifact_prepare = business_artifact_create_artifact_prepare

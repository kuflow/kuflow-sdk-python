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
from kuflow_rest._generated import _serialization


class PrincipalRetrieveRequest(_serialization.Model):
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


class PrincipalRetrieveResponse(_serialization.Model):
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


class TenantUserRetrieveRequest(_serialization.Model):
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


class TenantUserRetrieveResponse(_serialization.Model):
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


class ProcesFindRequest(_serialization.Model):
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


class ProcesFindResponse(_serialization.Model):
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


class ProcessRetrieveRequest(_serialization.Model):
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


class ProcessRetrieveResponse(_serialization.Model):
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


class ProcessEntityUpdateRequest(_serialization.Model):
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


class ProcessEntityUpdateResponse(_serialization.Model):
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


class ProcessEntityPatchRequest(_serialization.Model):
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


class ProcessEntityPatchResponse(_serialization.Model):
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


class ProcessMetadataUpdateRequest(_serialization.Model):
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


class ProcessMetadataUpdateResponse(_serialization.Model):
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


class ProcessMetadataPatchRequest(_serialization.Model):
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


class ProcessMetadataPatchResponse(_serialization.Model):
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


class ProcessInitiatorChangeRequest(_serialization.Model):
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


class ProcessInitiatorChangeResponse(_serialization.Model):
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


class ProcessItemFindRequest(_serialization.Model):
    _attribute_map = {
        "page": {"key": "page", "type": "int"},
        "size": {"key": "size", "type": "int"},
        "sorts": {"key": "sorts", "type": "[str]"},
        "tenant_ids": {"key": "tenantIds", "type": "[str]"},
        "process_ids": {"key": "processIds", "type": "[str]"},
        "types": {"key": "processIds", "type": "[ProcessItemType]"},
        "task_states": {"key": "taskStates", "type": "[ProcessItemTaskState]"},
        "process_item_definition_codes": {"key": "processItemDefinitionCodes", "type": "[str]"},
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


class ProcessItemFindResponse(_serialization.Model):
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


class ProcessItemRetrieveRequest(_serialization.Model):
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


class ProcessItemRetrieveResponse(_serialization.Model):
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


class ProcessItemCreateRequest(_serialization.Model):
    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "type": {"key": "type", "type": "ProcessItemType"},
        "process_id": {"key": "processId", "type": "str"},
        "owner_id": {"key": "ownerId", "type": "str"},
        "owner_email": {"key": "ownerEmail", "type": "str"},
        "process_item_definition_code": {"key": "processItemDefinitionCode", "type": "str"},
        "task": {"key": "task", "type": "ProcessItemTaskCreateParams"},
        "message": {"key": "task", "type": "ProcessItemMessageCreateParams"},
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


class ProcessItemCreateResponse(_serialization.Model):
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


class ProcessItemTaskCompleteRequest(_serialization.Model):
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


class ProcessItemTaskCompleteResponse(_serialization.Model):
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


class ProcessItemTaskClaimRequest(_serialization.Model):
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


class ProcessItemTaskClaimResponse(_serialization.Model):
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


class ProcessItemTaskAssignRequest(_serialization.Model):
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


class ProcessItemTaskAssignResponse(_serialization.Model):
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


class ProcessItemTaskDataUpdateRequest(_serialization.Model):
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


class ProcessItemTaskDataUpdateResponse(_serialization.Model):
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


class ProcessItemTaskDataPatchRequest(_serialization.Model):
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


class ProcessItemTaskDataPatchResponse(_serialization.Model):
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


class ProcessItemTaskLogAppendRequest(_serialization.Model):
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


class ProcessItemTaskLogAppendResponse(_serialization.Model):
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

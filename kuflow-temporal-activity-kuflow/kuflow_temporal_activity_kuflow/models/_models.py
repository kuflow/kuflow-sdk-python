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

from typing import Any, Dict, List, Optional

from kuflow_rest import models as models_rest
from kuflow_rest._generated import _serialization


########################
# For Workflows
########################


class WorkflowRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
    }

    def __init__(self, process_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_id: Identifier of the related created process
        """
        super().__init__(**kwargs)
        self.process_id = process_id


class WorkflowResponse(_serialization.Model):
    _attribute_map = {
        "message": {"key": "message", "type": "str"},
    }

    def __init__(self, message: Optional[str] = None, **kwargs: Any) -> None:
        """
        Parameters:
            message: Response message
        """
        super().__init__(**kwargs)
        self.message = message


class UserActionWorkflowRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "user_action_definition_code": {"key": "userActionDefinitionCode", "type": "str"},
        "user_action_id": {"key": "userActionId", "type": "str"},
        "requestor_principal_id": {"key": "requestorPrincipalId", "type": "str"},
    }

    def __init__(
        self,
        process_id: str,
        user_action_definition_code: str,
        user_action_id: str,
        requestor_principal_id: str,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_id: Identifier of the related process
            user_action_definition_code: Code of the user action definition
            user_action_id: Identifier of the user action
            requestor_principal_id: Identifier of the principal that request the user action
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.user_action_definition_code = user_action_definition_code
        self.user_action_id = user_action_id
        self.requestor_principal_id = requestor_principal_id


class UserActionWorkflowResponse(_serialization.Model):
    _attribute_map = {
        "message": {"key": "message", "type": "str"},
    }

    def __init__(self, message: Optional[str] = None, **kwargs: Any) -> None:
        """
        Parameters:
            message: User action message response
        """
        super().__init__(**kwargs)
        self.message = message


########################
# For Activities
########################


class RetrievePrincipalRequest(_serialization.Model):
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


class RetrievePrincipalResponse(_serialization.Model):
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


class FindProcessesRequest(_serialization.Model):
    _attribute_map = {
        "page": {"key": "page", "type": "int"},
        "size": {"key": "size", "type": "int"},
        "sorts": {"key": "sorts", "type": "[str]"},
    }

    def __init__(
        self, page: Optional[int] = None, size: Optional[int] = None, sorts: Optional[List[str]] = None, **kwargs: Any
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


class FindProcessesResponse(_serialization.Model):
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


class RetrieveProcessRequest(_serialization.Model):
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


class RetrieveProcessResponse(_serialization.Model):
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


class SaveProcessElementRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "element_definition_code": {"key": "elementDefinitionCode", "type": "str"},
        "element_values": {"key": "elementValues", "type": "[ProcessElementValue]"},
    }

    def __init__(
        self,
        process_id: str,
        element_definition_code: str,
        element_values: Optional[List[models_rest.ProcessElementValue]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_id: Process identifier to update
            element_definition_code: Element definition code
            element_values: Element values
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.element_definition_code = element_definition_code
        self.element_values = element_values or []


class SaveProcessElementResponse(_serialization.Model):
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


class DeleteProcessElementRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "element_definition_code": {"key": "elementDefinitionCode", "type": "str"},
    }

    def __init__(self, process_id: str, element_definition_code: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_id: Process related
            element_definition_code: Code of the element to delete
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.element_definition_code = element_definition_code


class DeleteProcessElementResponse(_serialization.Model):
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


class ChangeProcessInitiatorRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "email": {"key": "email", "type": "str"},
        "principal_id": {"key": "principalId", "type": "str"},
    }

    def __init__(
        self, process_id: str, email: Optional[str] = None, principal_id: Optional[str] = None, **kwargs: Any
    ) -> None:
        """
        Parameters:
            process_id: Process identifier to which want to change the initiator
            email: User email that want to use to assign the process. Attribute :email or :principal_id must be set.
            principal_id: Principal id that want to use to assign the process.
                          Attribute :email or :principal_id must be set.
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.email = email
        self.principal_id = principal_id


class ChangeProcessInitiatorResponse(_serialization.Model):
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


class FindTaskRequest(_serialization.Model):
    _attribute_map = {
        "page": {"key": "page", "type": "int"},
        "size": {"key": "size", "type": "int"},
        "sorts": {"key": "sorts", "type": "[str]"},
        "process_ids": {"key": "processIds", "type": "[str]"},
        "states": {"key": "states", "type": "[TaskState]"},
        "task_definition_codes": {"key": "taskDefinitionCodes", "type": "[str]"},
    }

    def __init__(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        sorts: Optional[List[str]] = None,
        process_ids: Optional[List[str]] = None,
        states: Optional[List[models_rest.TaskState]] = None,
        task_definition_codes: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            page: Page requested, 0-index
            size: Page size
            sorts: Sorting criteria in the format: property{,asc|desc}. Example: name,desc
            process_ids: Filter tasks by the process identifiers
            states: Filter tasks by the states
            task_definition_codes: Filter tasks by the task_definition_codes
        """
        super().__init__(**kwargs)
        self.page = page
        self.size = size
        self.sorts = sorts
        self.process_ids = process_ids
        self.states = states
        self.task_definition_codes = task_definition_codes


class FindTaskResponse(_serialization.Model):
    _attribute_map = {
        "tasks": {"key": "tasks", "type": "TaskPage"},
    }

    def __init__(self, tasks: models_rest.TaskPage, **kwargs: Any) -> None:
        """
        Parameters:
            tasks: Task page that math the requested criteria
        """
        super().__init__(**kwargs)
        self.tasks = tasks


class RetrieveTaskRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
    }

    def __init__(self, task_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            task_id: Task identifier to retrieve
        """
        super().__init__(**kwargs)
        self.task_id = task_id


class RetrieveTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task data
        """
        super().__init__(**kwargs)
        self.task = task


class CreateTaskRequest(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task to create
        """
        super().__init__(**kwargs)
        self.task = task


class CreateTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task created
        """
        super().__init__(**kwargs)
        self.task = task


class CompleteTaskRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
    }

    def __init__(self, task_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            task_id: Task identifier to mark as completed
        """
        super().__init__(**kwargs)
        self.task_id = task_id


class CompleteTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task updated
        """
        super().__init__(**kwargs)
        self.task = task


class ClaimTaskRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
    }

    def __init__(self, task_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            task_id: Task identifier to claim by the requestor
        """
        super().__init__(**kwargs)
        self.task_id = task_id


class ClaimTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task claimed
        """
        super().__init__(**kwargs)
        self.task = task


class AssignTaskRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
        "email": {"key": "email", "type": "str"},
        "principal_id": {"key": "principalId", "type": "str"},
    }

    def __init__(
        self, task_id: str, email: Optional[str] = None, principal_id: Optional[str] = None, **kwargs: Any
    ) -> None:
        """
        Parameters:
            task_id: Task to assign to the email or principal_id selected
            email: User email that want to use to assign the task. Attribute :email or principal_id must be set
            principal_id: Principal id that want to use to assign the task. Attribute _email or principal_id must be set
        """
        super().__init__(**kwargs)
        self.task_id = task_id
        self.email = email
        self.principal_id = principal_id


class AssignTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task updated
        """
        super().__init__(**kwargs)
        self.task = task


class SaveTaskElementRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
        "element_definition_code": {"key": "elementDefinitionCode", "type": "str"},
        "element_values": {"key": "elementValues", "type": "[TaskElementValue]"},
    }

    def __init__(
        self,
        task_id: str,
        element_definition_code: str,
        element_values: Optional[List[models_rest.TaskElementValue]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            task_id: Task to update
            element_definition_code: Element definition code
            element_values: Element values
        """
        super().__init__(**kwargs)
        self.task_id = task_id
        self.element_definition_code = element_definition_code
        self.element_values = element_values or []


class SaveTaskElementResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task updated
        """
        super().__init__(**kwargs)
        self.task = task


class DeleteTaskElementRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
        "element_definition_code": {"key": "elementDefinitionCode", "type": "str"},
    }

    def __init__(self, task_id: str, element_definition_code: str, **kwargs: Any) -> None:
        """
        Parameters:
            task_id: Task to update
            element_definition_code: Element definition code to delete all values
        """
        super().__init__(**kwargs)
        self.task_id = task_id
        self.element_definition_code = element_definition_code


class DeleteTaskElementResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task updated
        """
        super().__init__(**kwargs)
        self.task = task


class DeleteTaskElementValueDocumentRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
        "document_id": {"key": "documentId", "type": "str"},
    }

    def __init__(self, task_id: str, document_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            task_id: Task to update
            document_id: Document id to delete updated
        """
        super().__init__(**kwargs)
        self.task_id = task_id
        self.document_id = document_id


class DeleteTaskElementValueDocumentResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task updated
        """
        super().__init__(**kwargs)
        self.task = task


class SaveTaskJsonFormsValueDataRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
        "data": {"key": "data", "type": "{object}"},
    }

    def __init__(self, task_id: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        """
        Parameters:
            task_id: Task to update
            data: json data to save
        """
        super().__init__(**kwargs)
        self.task_id = task_id
        self.data = data or {}


class SaveTaskJsonFormsValueDataResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task updated
        """
        super().__init__(**kwargs)
        self.task = task


class AppendTaskLogRequest(_serialization.Model):
    _attribute_map = {
        "task_id": {"key": "taskId", "type": "str"},
        "log": {"key": "log", "type": "Log"},
    }

    def __init__(self, task_id: str, log: models_rest.Log, **kwargs: Any) -> None:
        """
        Parameters:
            task_id: Task to update
            log: Log data to add to the task
        """
        super().__init__(**kwargs)
        self.task_id = task_id
        self.log = log


class AppendTaskLogResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task, **kwargs: Any) -> None:
        """
        Parameters:
            task: Task updated
        """
        super().__init__(**kwargs)
        self.task = task

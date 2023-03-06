# coding=utf-8
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

from typing import List, Optional

from kuflow_rest._generated import _serialization
from kuflow_rest import models as models_rest

########################
# For Workflows
########################


class WorkflowRequest(_serialization.Model):
    _attribute_map = {
        "processId": {"key": "processId", "type": "str"},
    }

    def __init__(self, processId: str):
        self.processId = processId


class WorkflowResponse(_serialization.Model):
    _attribute_map = {
        "message": {"key": "message", "type": "str"},
    }

    def __init__(self, message: Optional[str] = None):
        self.message = message


class UserActionWorkflowRequest(_serialization.Model):
    _attribute_map = {
        "processId": {"key": "processId", "type": "str"},
        "userActionDefinitionCode": {"key": "userActionDefinitionCode", "type": "str"},
        "userActionId": {"key": "userActionId", "type": "str"},
        "requestorPrincipalId": {"key": "requestorPrincipalId", "type": "str"},
    }

    def __init__(self, processId: str, userActionDefinitionCode: str, userActionId: str, requestorPrincipalId: str):
        self.processId = processId
        self.userActionDefinitionCode = userActionDefinitionCode
        self.userActionId = userActionId
        self.requestorPrincipalId = requestorPrincipalId


class UserActionWorkflowResponse(_serialization.Model):
    _attribute_map = {
        "message": {"key": "message", "type": "str"},
    }

    def __init__(self, message: Optional[str] = None):
        self.message = message


########################
# For Activities
########################


class RetrievePrincipalRequest(_serialization.Model):
    _attribute_map = {
        "principalId": {"key": "principalId", "type": "str"},
    }

    def __init__(self, principalId: str):
        self.principalId = principalId


class RetrievePrincipalResponse(_serialization.Model):
    _attribute_map = {
        "principal": {"key": "principal", "type": "Principal"},
    }

    def __init__(self, principal: models_rest.Principal):
        self.principal = principal


class FindProcessesRequest(_serialization.Model):
    _attribute_map = {
        "page": {"key": "page", "type": "int"},
        "size": {"key": "size", "type": "int"},
        "sorts": {"key": "sorts", "type": "[str]"},
    }

    def __init__(self, page: Optional[int] = None, size: Optional[int] = None, sorts: Optional[List[str]] = None):
        self.page = page
        self.size = size
        self.sorts = sorts


class FindProcessesResponse(_serialization.Model):
    _attribute_map = {
        "processes": {"key": "processes", "type": "ProcessPage"},
    }

    def __init__(self, processes: models_rest.ProcessPage):
        self.processes = processes


class RetrieveProcessRequest(_serialization.Model):
    _attribute_map = {
        "processId": {"key": "processId", "type": "str"},
    }

    def __init__(self, processId: str):
        self.processId = processId


class RetrieveProcessResponse(_serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process):
        self.process = process


class SaveProcessElementRequest(_serialization.Model):
    _attribute_map = {
        "processId": {"key": "processId", "type": "str"},
        "elementDefinitionCode": {"key": "elementDefinitionCode", "type": "str"},
        "elementValues": {"key": "elementValues", "type": "[ProcessElementValue]"},
    }

    def __init__(
        self, processId: str, elementDefinitionCode: str, elementValues: List["models_rest.ProcessElementValue"]
    ):
        self.processId = processId
        self.elementDefinitionCode = elementDefinitionCode
        self.elementValues = elementValues


class SaveProcessElementResponse(_serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process):
        self.process = process


class DeleteProcessElementRequest(_serialization.Model):
    _attribute_map = {
        "processId": {"key": "processId", "type": "str"},
        "elementDefinitionCode": {"key": "elementDefinitionCode", "type": "str"},
    }

    def __init__(self, processId: str, elementDefinitionCode: str):
        self.processId = processId
        self.elementDefinitionCode = elementDefinitionCode


class DeleteProcessElementResponse(_serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process):
        self.process = process


class CompleteProcessRequest(_serialization.Model):
    _attribute_map = {
        "processId": {"key": "processId", "type": "str"},
    }

    def __init__(self, processId: str):
        self.processId = processId


class CompleteProcessResponse(_serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process):
        self.process = process


class ChangeProcessInitiatorRequest(_serialization.Model):
    """
    processId: Required
    email: User email that want to use to assign the task. Attribute :email or principalId must be set.
    principalId: Principal id that want to use to assign the task. Attribute email or principalId must be set.
    """

    _attribute_map = {
        "processId": {"key": "processId", "type": "str"},
        "email": {"key": "email", "type": "str"},
        "principalId": {"key": "principalId", "type": "str"},
    }

    def __init__(self, processId: str, email: Optional[str] = None, principalId: Optional[str] = None):
        self.processId = processId
        self.email = email
        self.principalId = principalId


class ChangeProcessInitiatorResponse(_serialization.Model):
    _attribute_map = {
        "process": {"key": "process", "type": "Process"},
    }

    def __init__(self, process: models_rest.Process):
        self.process = process


class FindTaskRequest(_serialization.Model):
    _attribute_map = {
        "page": {"key": "page", "type": "int"},
        "size": {"key": "size", "type": "int"},
        "sorts": {"key": "sorts", "type": "[str]"},
        "processIds": {"key": "processIds", "type": "[str]"},
        "states": {"key": "states", "type": "[TaskState]"},
        "taskDefinitionCodes": {"key": "taskDefinitionCodes", "type": "[str]"},
    }

    def __init__(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        sorts: Optional[List[str]] = None,
        processIds: Optional[List[str]] = None,
        states: Optional[List[models_rest.TaskState]] = None,
        taskDefinitionCodes: Optional[List[str]] = None,
    ):
        self.page = page
        self.size = size
        self.sorts = sorts
        self.processIds = processIds
        self.states = states
        self.taskDefinitionCodes = taskDefinitionCodes


class FindTaskResponse(_serialization.Model):
    _attribute_map = {
        "tasks": {"key": "tasks", "type": "TaskPage"},
    }

    def __init__(self, tasks: models_rest.TaskPage):
        self.tasks = tasks


class RetrieveTaskRequest(_serialization.Model):
    _attribute_map = {
        "taskId": {"key": "taskId", "type": "str"},
    }

    def __init__(self, taskId: str):
        self.taskId = taskId


class RetrieveTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class CreateTaskRequest(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class CreateTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class CompleteTaskRequest(_serialization.Model):
    _attribute_map = {
        "taskId": {"key": "taskId", "type": "str"},
    }

    def __init__(self, taskId: str):
        self.taskId = taskId


class CompleteTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class ClaimTaskRequest(_serialization.Model):
    _attribute_map = {
        "taskId": {"key": "taskId", "type": "str"},
    }

    def __init__(self, taskId: str):
        self.taskId = taskId


class ClaimTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class AssignTaskRequest(_serialization.Model):
    """
    taskId: Required
    email: User email that want to use to assign the task. Attribute :email or principalId must be set.
    principalId: Principal id that want to use to assign the task. Attribute email or principalId must be set.
    """

    _attribute_map = {
        "taskId": {"key": "taskId", "type": "str"},
        "email": {"key": "email", "type": "str"},
        "principalId": {"key": "principalId", "type": "str"},
    }

    def __init__(self, taskId: str, email: Optional[str] = None, principalId: Optional[str] = None):
        self.taskId = taskId
        self.email = email
        self.principalId = principalId


class AssignTaskResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class SaveTaskElementRequest(_serialization.Model):
    _attribute_map = {
        "taskId": {"key": "taskId", "type": "str"},
        "elementDefinitionCode": {"key": "elementDefinitionCode", "type": "str"},
        "elementValues": {"key": "elementValues", "type": "[TaskElementValue]"},
    }

    def __init__(self, taskId: str, elementDefinitionCode: str, elementValues: List["models_rest.TaskElementValue"]):
        self.taskId = taskId
        self.elementDefinitionCode = elementDefinitionCode
        self.elementValues = elementValues


class SaveTaskElementResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class DeleteTaskElementRequest(_serialization.Model):
    _attribute_map = {
        "taskId": {"key": "taskId", "type": "str"},
        "elementDefinitionCode": {"key": "elementDefinitionCode", "type": "str"},
    }

    def __init__(self, taskId: str, elementDefinitionCode: str):
        self.taskId = taskId
        self.elementDefinitionCode = elementDefinitionCode


class DeleteTaskElementResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class DeleteTaskElementValueDocumentRequest(_serialization.Model):
    _attribute_map = {
        "taskId": {"key": "taskId", "type": "str"},
        "documentId": {"key": "documentId", "type": "str"},
    }

    def __init__(self, taskId: str, documentId: str):
        self.taskId = taskId
        self.documentId = documentId


class DeleteTaskElementValueDocumentResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task


class AppendTaskLogRequest(_serialization.Model):
    _attribute_map = {
        "taskId": {"key": "taskId", "type": "str"},
        "log": {"key": "log", "type": "Log"},
    }

    def __init__(self, taskId: str, log: models_rest.Log):
        self.taskId = taskId
        self.log = log


class AppendTaskLogResponse(_serialization.Model):
    _attribute_map = {
        "task": {"key": "task", "type": "Task"},
    }

    def __init__(self, task: models_rest.Task):
        self.task = task

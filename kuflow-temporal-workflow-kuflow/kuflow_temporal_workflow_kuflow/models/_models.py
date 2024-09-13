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

from typing import TYPE_CHECKING, Any, Optional

from kuflow_rest._generated import _serialization


if TYPE_CHECKING:
    from .. import models as _models

KUFLOW_ENGINE_SIGNAL_PROCESS_ITEM = "KuFlow_Engine_Signal_Process_Item"


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


class RobotWorkflowRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "task_id": {"key": "taskId", "type": "str"},
    }

    def __init__(self, process_id: str, task_id: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_id: Identifier of the related created process
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.task_id = task_id


class RobotWorkflowResponse(_serialization.Model):
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


class SignalProcessItemPayload(_serialization.Model):
    _attribute_map = {
        "task_definition_code": {"key": "taskDefinitionCode", "type": "str"},
        "data_structure_data_definition_code": {"key": "dataStructureDataDefinitionCode", "type": "str"},
    }

    def __init__(
        self, task_definition_code: Optional[str], data_structure_data_definition_code: Optional[str], **kwargs: Any
    ) -> None:
        """
        Parameters:
            task_definition_code: Task definition code
            data_structure_data_definition_code: Data structure data definition code
        """
        super().__init__(**kwargs)
        self.task_definition_code = task_definition_code
        self.data_structure_data_definition_code = data_structure_data_definition_code


class SignalProcessItem(_serialization.Model):
    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "type": {"key": "type", "type": "str"},
        "payload": {"key": "payload", "type": "SignalProcessItemPayload"},
    }

    def __init__(
        self, id: str, type: "_models.SignalProcessItemType", payload: "_models.SignalProcessItemPayload", **kwargs: Any
    ) -> None:
        """
        Parameters:
            id: Process item Id
            type: Process item type
            payload: Process item signal payload
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.payload = payload
